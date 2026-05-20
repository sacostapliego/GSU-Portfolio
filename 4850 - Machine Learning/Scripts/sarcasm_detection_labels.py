import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


SCRIPT_STATE_VERSION = 2


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Classify tweets as sarcastic (1) or not sarcastic (0)."
	)
	parser.add_argument(
		"--input-path",
		type=Path,
		default=Path("dataset/election/data.csv"),
		help="Input TSV file path.",
	)
	parser.add_argument(
		"--model-path",
		type=Path,
		default=Path("models/sarcasm_model"),
		help="Local directory for helinivan/english-sarcasm-detector snapshot.",
	)
	parser.add_argument(
		"--write-every",
		type=int,
		default=500,
		help="Checkpoint write interval in processed rows.",
	)
	parser.add_argument(
		"--limit",
		type=int,
		default=None,
		help="Optional max rows to process for smoke tests.",
	)
	parser.add_argument(
		"--max-length",
		type=int,
		default=256,
		help="Tokenizer max sequence length.",
	)
	parser.add_argument(
		"--no-resume",
		action="store_true",
		help="Ignore checkpoint files and start from scratch.",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Write output to a separate file instead of overwriting input.",
	)
	parser.add_argument(
		"--dry-run-output",
		type=Path,
		default=None,
		help="Optional output path used only when --dry-run is enabled.",
	)
	return parser.parse_args()


def resolve_output_path(input_path: Path, dry_run: bool, dry_run_output: Optional[Path]) -> Path:
	if not dry_run:
		return input_path
	if dry_run_output is not None:
		return dry_run_output
	return input_path.with_suffix(".sarcasm.dryrun.csv")


def atomic_to_csv(df: pd.DataFrame, path: Path) -> None:
	tmp_path = path.with_suffix(path.suffix + ".tmp")
	df.to_csv(tmp_path, sep="\t", encoding="utf-8", index=False)
	tmp_path.replace(path)


def atomic_write_json(data: Dict[str, Any], path: Path) -> None:
	tmp_path = path.with_suffix(path.suffix + ".tmp")
	tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
	tmp_path.replace(path)


def required_model_files_exist(model_path: Path) -> None:
	if not model_path.exists() or not model_path.is_dir():
		raise FileNotFoundError(f"Model path not found or not a directory: {model_path}")

	required = ["config.json", "tokenizer_config.json"]
	missing = [name for name in required if not (model_path / name).exists()]

	has_tokenizer_assets = any(
		(model_path / name).exists() for name in ["tokenizer.json", "vocab.txt"]
	)
	if not has_tokenizer_assets:
		missing.append("tokenizer.json or vocab.txt")

	has_weights = any(
		(model_path / name).exists() for name in ["model.safetensors", "pytorch_model.bin"]
	)
	if not has_weights:
		missing.append("model.safetensors or pytorch_model.bin")

	if missing:
		raise FileNotFoundError(
			f"Model path is missing required artifacts: {', '.join(missing)}"
		)


def load_dataset(input_path: Path) -> pd.DataFrame:
	if not input_path.exists():
		raise FileNotFoundError(f"Input file not found: {input_path}")

	df = pd.read_csv(input_path, sep="\t")
	if "rawTweet" not in df.columns:
		raise ValueError("Input file must contain a 'rawTweet' column.")
	if "sarcasm_label" not in df.columns:
		df["sarcasm_label"] = pd.NA
	return df


def normalize_text(text: str) -> str:
	text = text.strip().lower()
	text = re.sub(r"\s+", " ", text)
	return text


def init_working_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	work = df.copy()
	if "_sarcasm_labeled" not in work.columns:
		work["_sarcasm_labeled"] = work["sarcasm_label"].isin([0, 1]).astype(int)
	return work


def map_prediction_to_binary(class_id: int, id2label: Optional[Dict[Any, Any]]) -> int:
	if id2label:
		label_name = id2label.get(class_id)
		if label_name is None:
			label_name = id2label.get(str(class_id))
		if label_name is not None:
			normalized = str(label_name).strip().lower()
			if normalized in {"0", "label_0", "not sarcastic", "non sarcastic", "not_sarcastic"}:
				return 0
			if normalized in {"1", "label_1", "sarcastic"}:
				return 1
	# Documented helinivan mapping fallback.
	return 1 if int(class_id) == 1 else 0


def load_classifier(
	model_path: Path,
) -> Tuple[AutoTokenizer, AutoModelForSequenceClassification, torch.device, Dict[str, Any]]:
	required_model_files_exist(model_path)

	tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
	model_obj, loading_info = AutoModelForSequenceClassification.from_pretrained(
		str(model_path),
		local_files_only=True,
		output_loading_info=True,
		ignore_mismatched_sizes=False,
	)

	missing_keys = list(loading_info.get("missing_keys", []))
	unexpected_keys = list(loading_info.get("unexpected_keys", []))
	base_prefix = getattr(model_obj, "base_model_prefix", "bert")
	critical_prefixes = (f"{base_prefix}.", "classifier.")
	critical_missing = [k for k in missing_keys if k.startswith(critical_prefixes)]
	if critical_missing:
		raise RuntimeError(
			"Critical checkpoint weights are missing; refusing to continue. "
			f"Examples: {critical_missing[:8]}"
		)

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	model_obj = model_obj.to(device)
	if device.type == "cpu":
		# Avoid float16 instability on CPU for reproducible logits.
		model_obj = model_obj.float()
	model_obj.eval()

	diag = {
		"model_type": getattr(model_obj.config, "model_type", "unknown"),
		"base_model_prefix": base_prefix,
		"num_labels": int(getattr(model_obj.config, "num_labels", 2)),
		"id2label": getattr(model_obj.config, "id2label", {}) or {},
		"missing_keys": missing_keys,
		"unexpected_keys": unexpected_keys,
		"mismatched_keys": list(loading_info.get("mismatched_keys", [])),
		"torch_dtype": str(next(model_obj.parameters()).dtype),
	}
	return tokenizer, model_obj, device, diag


def infer_sarcasm_label(
	text: str,
	tokenizer: AutoTokenizer,
	model: AutoModelForSequenceClassification,
	device: torch.device,
	max_length: int,
) -> int:
	encoded = tokenizer(
		[text],
		return_tensors="pt",
		truncation=True,
		padding=True,
		max_length=max_length,
	)
	encoded = {k: v.to(device) for k, v in encoded.items()}

	with torch.no_grad():
		outputs = model(**encoded)

	class_id = int(outputs.logits.argmax(dim=1).item())
	id2label = getattr(model.config, "id2label", None)
	return map_prediction_to_binary(class_id, id2label)


def build_model_signature(model_path: Path, model_diag: Dict[str, Any]) -> Dict[str, Any]:
	return {
		"state_version": SCRIPT_STATE_VERSION,
		"resolved_model_path": str(model_path.resolve()),
		"model_type": model_diag.get("model_type"),
		"num_labels": model_diag.get("num_labels"),
	}


def save_checkpoint(
	df: pd.DataFrame,
	checkpoint_path: Path,
	state_path: Path,
	counts: Dict[str, int],
	last_completed_index: int,
	input_path: Path,
	model_path: Path,
	model_signature: Dict[str, Any],
	cache: Dict[str, int],
) -> None:
	checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
	atomic_to_csv(df, checkpoint_path)

	state = {
		"input_path": str(input_path),
		"model_path": str(model_path),
		"model_signature": model_signature,
		"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
		"total_rows": int(len(df)),
		"processed_rows": int(counts["processed"]),
		"count_1": int(counts["1"]),
		"count_0": int(counts["0"]),
		"failures": int(counts["failures"]),
		"cache_hits": int(counts["cache_hits"]),
		"cache_size": int(len(cache)),
		"last_completed_index": int(last_completed_index),
		"next_index": int(last_completed_index + 1),
		"text_cache": cache,
	}
	atomic_write_json(state, state_path)


def load_checkpoint_if_compatible(
	df: pd.DataFrame,
	checkpoint_path: Path,
	state_path: Path,
	model_signature: Dict[str, Any],
) -> Tuple[pd.DataFrame, int, Dict[str, int]]:
	if not checkpoint_path.exists() or not state_path.exists():
		return df, 0, {}

	checkpoint_df = pd.read_csv(checkpoint_path, sep="\t")
	state = json.loads(state_path.read_text(encoding="utf-8"))

	if len(checkpoint_df) != len(df):
		raise ValueError("checkpoint row count mismatch")
	if "sarcasm_label" not in checkpoint_df.columns:
		raise ValueError("checkpoint missing sarcasm_label column")

	state_sig = state.get("model_signature", {})
	if state_sig != model_signature:
		raise ValueError("checkpoint model signature mismatch")

	start_index = int(state.get("next_index", 0))
	loaded_cache = state.get("text_cache", {})
	cache: Dict[str, int] = {}
	if isinstance(loaded_cache, dict):
		for k, v in loaded_cache.items():
			try:
				iv = int(v)
			except (TypeError, ValueError):
				continue
			if iv in (0, 1):
				cache[str(k)] = iv

	return checkpoint_df, start_index, cache


def main() -> int:
	args = parse_args()
	input_path = args.input_path
	output_path = resolve_output_path(input_path, args.dry_run, args.dry_run_output)
	checkpoint_path = output_path.with_suffix(".sarcasm.partial.csv")
	state_path = output_path.with_suffix(".sarcasm.partial.state.json")

	try:
		tokenizer, model, device, model_diag = load_classifier(args.model_path)
	except Exception as exc:
		print(f"Failed to load local model from {args.model_path}: {exc}")
		return 2

	model_signature = build_model_signature(args.model_path, model_diag)

	print("Model diagnostics:")
	print(f"  path={args.model_path.resolve()}")
	print(f"  model_type={model_diag['model_type']} base_prefix={model_diag['base_model_prefix']}")
	print(f"  num_labels={model_diag['num_labels']} id2label={model_diag['id2label']}")
	print(
		"  loading_info: "
		f"missing={len(model_diag['missing_keys'])} "
		f"unexpected={len(model_diag['unexpected_keys'])} "
		f"mismatched={len(model_diag['mismatched_keys'])}"
	)

	df = load_dataset(input_path)
	start_index = 0
	cache: Dict[str, int] = {}

	if not args.no_resume:
		try:
			df, start_index, cache = load_checkpoint_if_compatible(
				df=df,
				checkpoint_path=checkpoint_path,
				state_path=state_path,
				model_signature=model_signature,
			)
			if start_index > 0:
				print(f"Resuming from checkpoint at row index {start_index}.")
				print(f"Restored text cache entries: {len(cache)}")
		except Exception as exc:
			print(f"Ignoring checkpoint/state due to incompatibility: {exc}")

	work_df = init_working_dataframe(df)

	counts = {
		"processed": int((work_df["_sarcasm_labeled"] == 1).sum()),
		"1": int((work_df["sarcasm_label"] == 1).sum()),
		"0": int((work_df["sarcasm_label"] == 0).sum()),
		"failures": 0,
		"cache_hits": 0,
	}

	total_rows = len(work_df)
	end_index = total_rows if args.limit is None else min(total_rows, args.limit)

	mode_name = "DRY RUN" if args.dry_run else "FULL RUN"
	print(f"Mode: {mode_name}")
	print(f"Input path: {input_path}")
	print(f"Output path: {output_path}")
	print(f"Device: {device} dtype={model_diag['torch_dtype']}")
	print(f"Rows in dataset: {total_rows}")
	print(f"Processing range: [{start_index}, {end_index})")

	last_completed_index = max(start_index - 1, -1)

	try:
		for idx in range(start_index, end_index):
			if int(work_df.at[idx, "_sarcasm_labeled"]) == 1:
				last_completed_index = idx
				continue

			raw_tweet = work_df.at[idx, "rawTweet"]
			tweet_text = "" if pd.isna(raw_tweet) else str(raw_tweet)

			old_label = work_df.at[idx, "sarcasm_label"]
			success = False
			new_label: Optional[int] = None

			if tweet_text.strip() == "":
				new_label = 0
				success = True
			else:
				key = normalize_text(tweet_text)
				if key in cache:
					new_label = cache[key]
					counts["cache_hits"] += 1
					success = True
				else:
					try:
						new_label = infer_sarcasm_label(
							text=tweet_text,
							tokenizer=tokenizer,
							model=model,
							device=device,
							max_length=args.max_length,
						)
						cache[key] = int(new_label)
						success = True
					except Exception as exc:
						counts["failures"] += 1
						print(f"Row {idx}: inference failed ({exc}); preserving existing sarcasm_label.")

			if success and new_label is not None:
				work_df.at[idx, "sarcasm_label"] = int(new_label)
				work_df.at[idx, "_sarcasm_labeled"] = 1
				counts["processed"] += 1

				if pd.isna(old_label):
					if new_label == 1:
						counts["1"] += 1
					else:
						counts["0"] += 1
				else:
					try:
						old_int = int(old_label)
					except (TypeError, ValueError):
						old_int = None
					if old_int in (0, 1) and old_int != new_label:
						if old_int == 1:
							counts["1"] -= 1
						else:
							counts["0"] -= 1
						if new_label == 1:
							counts["1"] += 1
						else:
							counts["0"] += 1

				last_completed_index = idx

				if counts["processed"] % args.write_every == 0:
					save_checkpoint(
						df=work_df,
						checkpoint_path=checkpoint_path,
						state_path=state_path,
						counts=counts,
						last_completed_index=last_completed_index,
						input_path=input_path,
						model_path=args.model_path,
						model_signature=model_signature,
						cache=cache,
					)
					print(
						f"Checkpoint saved at row {idx}. processed={counts['processed']} "
						f"sarcastic={counts['1']} not_sarcastic={counts['0']} "
						f"failures={counts['failures']} cache_hits={counts['cache_hits']}"
					)

	except KeyboardInterrupt:
		print("Interrupted. Saving checkpoint before exit...")
		save_checkpoint(
			df=work_df,
			checkpoint_path=checkpoint_path,
			state_path=state_path,
			counts=counts,
			last_completed_index=last_completed_index,
			input_path=input_path,
			model_path=args.model_path,
			model_signature=model_signature,
			cache=cache,
		)
		print("Checkpoint saved. Re-run script to resume.")
		return 130

	final_df = work_df.drop(columns=["_sarcasm_labeled"], errors="ignore")
	output_path.parent.mkdir(parents=True, exist_ok=True)
	atomic_to_csv(final_df, output_path)

	if checkpoint_path.exists():
		checkpoint_path.unlink(missing_ok=True)
	if state_path.exists():
		state_path.unlink(missing_ok=True)

	print("Sarcasm labeling complete.")
	print(f"Output written to {output_path}")
	print(
		f"Summary: processed={counts['processed']} sarcastic={counts['1']} "
		f"not_sarcastic={counts['0']} failures={counts['failures']} "
		f"cache_size={len(cache)} cache_hits={counts['cache_hits']}"
	)
	return 0


if __name__ == "__main__":
	sys.exit(main())
