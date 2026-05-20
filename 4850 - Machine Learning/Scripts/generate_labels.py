import argparse
import json
from pydoc import text
import re
import sys
import time
from pathlib import Path
from typing import Dict, Tuple
from urllib import error, request

import pandas as pd


SYSTEM_PROMPT = (
	"You are a strict political stance classifier for US election tweets. "
	"Return exactly one integer token: 1 or 2, with no additional text. "
	"1 means the tweet is pro-Trump. "
	"2 means the tweet is pro-Biden. "
	"Do not output any other text."
)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Label election tweets with LM Studio (1=pro-Trump, 2=pro-Biden)."
	)
	parser.add_argument(
		"--input-path",
		type=Path,
		default=Path("dataset/election/data.csv"),
		help="Input TSV file path.",
	)
	parser.add_argument(
		"--base-url",
		type=str,
		default="http://127.0.0.1:1234/v1",
		help="LM Studio OpenAI-compatible base URL.",
	)
	parser.add_argument(
		"--model",
		type=str,
		default="local-model",
		help="Model identifier exposed by LM Studio.",
	)
	parser.add_argument(
		"--timeout",
		type=int,
		default=30,
		help="HTTP timeout in seconds.",
	)
	parser.add_argument(
		"--max-retries",
		type=int,
		default=3,
		help="Max retries for API errors.",
	)
	parser.add_argument(
		"--retry-delay",
		type=float,
		default=1.0,
		help="Base delay (seconds) between retries.",
	)
	parser.add_argument(
		"--write-every",
		type=int,
		default=50,
		help="Checkpoint write interval in processed rows.",
	)
	parser.add_argument(
		"--limit",
		type=int,
		default=None,
		help="Optional max number of rows to process for smoke testing.",
	)
	parser.add_argument(
		"--no-resume",
		action="store_true",
		help="Ignore checkpoint files and start from scratch.",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Write labeled output to a separate file instead of overwriting input.",
	)
	parser.add_argument(
		"--dry-run-output",
		type=Path,
		default=None,
		help="Optional output path used only when --dry-run is enabled.",
	)
	return parser.parse_args()


def normalize_base_url(base_url: str) -> str:
	return base_url.rstrip("/")


def extract_label(text: str) -> int:
    if not text:
        return 0
    
    stripped = text.strip()
    if stripped in {"1", "2"}:
        return int(stripped)

    match = re.search(r"\b([12])\b", stripped)
    if not match:
        return 0

    value = int(match.group(1))
    return value if value in {1, 2} else 0

def call_lm_studio(
	tweet: str,
	base_url: str,
	model: str,
	timeout: int,
	max_retries: int,
	retry_delay: float,
) -> Tuple[int, str]:
	url = f"{normalize_base_url(base_url)}/chat/completions"
	payload = {
		"model": model,
		"temperature": 0,
		"max_tokens": 300,
		"messages": [
			{"role": "system", "content": SYSTEM_PROMPT},
			{
				"role": "user",
				"content": f"Tweet:\n{tweet}\n\nReturn only 1 or 2.",
			},
		],
	}
	data = json.dumps(payload).encode("utf-8")
	headers = {"Content-Type": "application/json"}

	last_error = "unknown error"
	for attempt in range(1, max_retries + 1):
		req = request.Request(url=url, data=data, headers=headers, method="POST")
		try:
			with request.urlopen(req, timeout=timeout) as resp:
				body = resp.read().decode("utf-8", errors="ignore")
			obj = json.loads(body)
			content = obj["choices"][0]["message"]["content"]
			return extract_label(content), content
		except (error.HTTPError, error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
			last_error = str(exc)
			if attempt < max_retries:
				time.sleep(retry_delay * attempt)

	return 0, f"ERROR: {last_error}"


def atomic_to_csv(df: pd.DataFrame, path: Path) -> None:
	tmp_path = path.with_suffix(path.suffix + ".tmp")
	df.to_csv(tmp_path, sep="\t", encoding="utf-8", index=False)
	tmp_path.replace(path)


def atomic_write_json(data: Dict, path: Path) -> None:
	tmp_path = path.with_suffix(path.suffix + ".tmp")
	tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
	tmp_path.replace(path)


def save_checkpoint(
	df: pd.DataFrame,
	checkpoint_path: Path,
	state_path: Path,
	counts: Dict[str, int],
	last_completed_index: int,
	input_path: Path,
	model: str,
) -> None:
	checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
	atomic_to_csv(df, checkpoint_path)

	state = {
		"input_path": str(input_path),
		"model": model,
		"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
		"total_rows": int(len(df)),
		"processed_rows": int(counts["processed"]),
		"count_1": int(counts["1"]),
		"count_2": int(counts["2"]),
		"count_0": int(counts["0"]),
		"api_failures": int(counts["failures"]),
		"last_completed_index": int(last_completed_index),
		"next_index": int(last_completed_index + 1),
	}
	atomic_write_json(state, state_path)


def load_dataset(input_path: Path) -> pd.DataFrame:
	if not input_path.exists():
		raise FileNotFoundError(f"Input file not found: {input_path}")

	df = pd.read_csv(input_path, sep="\t")
	if "rawTweet" not in df.columns:
		raise ValueError("Input file must contain a 'rawTweet' column.")

	if "llm_label" not in df.columns:
		df["llm_label"] = 0

	return df


def init_working_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	work = df.copy()
	if "_lm_labeled" not in work.columns:
		work["_lm_labeled"] = 0
	return work


def resolve_output_path(input_path: Path, dry_run: bool, dry_run_output: Path = None) -> Path:
	if not dry_run:
		return input_path
	if dry_run_output is not None:
		return dry_run_output

	return input_path.with_suffix(".dryrun.csv")


def main() -> int:
	args = parse_args()
	input_path = args.input_path
	output_path = resolve_output_path(input_path, args.dry_run, args.dry_run_output)
	checkpoint_path = output_path.with_suffix(".partial.csv")
	state_path = output_path.with_suffix(".partial.state.json")

	df = load_dataset(input_path)
	start_index = 0

	if not args.no_resume and checkpoint_path.exists() and state_path.exists():
		try:
			checkpoint_df = pd.read_csv(checkpoint_path, sep="\t")
			state = json.loads(state_path.read_text(encoding="utf-8"))
			if len(checkpoint_df) == len(df):
				df = checkpoint_df
				start_index = int(state.get("next_index", 0))
				print(f"Resuming from checkpoint at row index {start_index}.")
			else:
				print("Checkpoint row count mismatch. Starting from scratch.")
		except Exception as exc:
			print(f"Failed to read checkpoint/state ({exc}). Starting from scratch.")

	work_df = init_working_dataframe(df)

	counts = {
		"processed": int((work_df["_lm_labeled"] == 1).sum()),
		"1": int((work_df["llm_label"] == 1).sum()),
		"2": int((work_df["llm_label"] == 2).sum()),
		"0": int(((work_df["_lm_labeled"] == 1) & ~work_df["llm_label"].isin([1, 2])).sum()),
		"failures": 0,
	}

	total_rows = len(work_df)
	end_index = total_rows if args.limit is None else min(total_rows, args.limit)

	mode_name = "DRY RUN" if args.dry_run else "FULL RUN"
	print(f"Mode: {mode_name}")
	print(f"Input path: {input_path}")
	print(f"Output path: {output_path}")
	print(f"Rows in dataset: {total_rows}")
	print(f"Processing range: [{start_index}, {end_index})")

	last_completed_index = max(start_index - 1, -1)

	try:
		for idx in range(start_index, end_index):
			if int(work_df.at[idx, "_lm_labeled"]) == 1:
				last_completed_index = idx
				continue

			raw_tweet = work_df.at[idx, "rawTweet"]
			tweet_text = "" if pd.isna(raw_tweet) else str(raw_tweet)

			if tweet_text.strip() == "":
				label = 0
				response_text = "EMPTY_TWEET"
			else:
				label, response_text = call_lm_studio(
					tweet=tweet_text,
					base_url=args.base_url,
					model=args.model,
					timeout=args.timeout,
					max_retries=args.max_retries,
					retry_delay=args.retry_delay,
				)
				if response_text.startswith("ERROR:"):
					counts["failures"] += 1

			work_df.at[idx, "llm_label"] = int(label)
			work_df.at[idx, "_lm_labeled"] = 1

			counts["processed"] += 1
			if label == 1:
				counts["1"] += 1
			elif label == 2:
				counts["2"] += 1
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
					model=args.model,
				)
				print(
					f"Checkpoint saved at row {idx}. "
					f"processed={counts['processed']} 1={counts['1']} 2={counts['2']} 0={counts['0']}"
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
			model=args.model,
		)
		print("Checkpoint saved. Re-run script to resume.")
		return 130

	final_df = work_df.drop(columns=["_lm_labeled"], errors="ignore")
	output_path.parent.mkdir(parents=True, exist_ok=True)
	atomic_to_csv(final_df, output_path)

	if checkpoint_path.exists():
		checkpoint_path.unlink(missing_ok=True)
	if state_path.exists():
		state_path.unlink(missing_ok=True)

	print("Labeling complete.")
	print(f"Output written to {output_path}")
	print(
		f"Summary: processed={counts['processed']} "
		f"1={counts['1']} 2={counts['2']} 0={counts['0']} failures={counts['failures']}"
	)
	return 0


if __name__ == "__main__":
	sys.exit(main())
