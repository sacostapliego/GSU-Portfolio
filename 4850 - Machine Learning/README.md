# InfoVGAE
The source code for SIGIR 2022 paper: "Unsupervised Belief Representation Learning with Information-Theoretic Variational Graph Auto-Encoders"

## Training

To run InfoVGAE on Eurovision dataset:

```
python3 main.py --config_name InfoVGAE_eurovision_3D
```

To run InfoVGAE on Election dataset:

```
python3 main.py --config_name InfoVGAE_election_3D
```

To run InfoVGAE on Voteview 105th Congress dataset:
```
python3 main.py --config_name InfoVGAE_bill_3D
```

To run InfoVGAE on TIMME dataset:
```
python3 main.py --config_name InfoVGAE_timme_3D
```

To run InfoVGAE on TIMME dataset with follow (friend) links:
```
python3 main.py --config_name InfoVGAE_timme_follow_3D
```

The `embeddings`, `labels`, `figures`, and `top-k tweets` (only applicable for Twitter datasets), etc, will be saved in `./output`

## Dataset

We uploaded the pre-processed datasets with smaller size, due to the file size limits of Github. The datasets are located in `dataset/election`, `dataset/eurovision`, and `dataset/bill`. It may takes some time to clone this repo (`297MB`). After cloning this repo, please run:

```
unzip dataset/bill/bmap2.pkl.zip; unzip dataset/bill/data_80_115.pkl.zip
```

## Evaluation

Evaluation will be automaticly triggered after the training process. To evaluate again, modify the `evaluator.init_from_dir()` in `evaluate.py`.

## Other arguments for training:

> General

`--use_cuda`: training with GPU

`--epochs`: iterations for training

`--learning_rate`: learning rate for training

`--device`: which gpu to use. empty for cpu.

`--num_process`: num process for pandas processing

> Data

`--data_path`: csv path for data file

`--stopword_path`: stopword path for text parsing

`--kthreshold`: tweet count threshold to filter not popular tweets.

`--uthreshold`: user count threshold to filter not popular users.

> For InfoVGAE model

`--hidden1_dim`: the latent space dimension of first layer

`--hidden2_dim`: the latent space dimension of target layer

`--use_cross_entropy_loss`: whether to use an additional cross-entropy loss term based on llm-generated labels

> Result

`--output_path` path to save the result

## Generate Election Labels With LM Studio

Use the helper script to label tweets in `dataset/election/data.csv` from the `rawTweet` column.
Predictions are written to a new `llm_label` column, and the existing `label` column is preserved.

- Label `1`: pro-Trump
- Label `2`: pro-Biden
- Label `0`: unclear/neutral/unparseable response

Start LM Studio server first (OpenAI-compatible API), then run:

```bash
python Scripts/generate_labels.py --model local-model
```

Optional useful flags:

```bash
python Scripts/generate_labels.py --model local-model --write-every 50 --max-retries 3
```

Dry-run on first N rows without overwriting `dataset/election/data.csv`:

```bash
python Scripts/generate_labels.py --model local-model --dry-run --limit 200
```

By default dry-run writes to `dataset/election/data.dryrun.csv`. You can set a custom path with `--dry-run-output`.

Checkpoint/resume behavior:

- Partial progress is periodically saved to `dataset/election/data.partial.csv`.
- Resume metadata is saved to `dataset/election/data.partial.state.json`.
- If interrupted, re-run the same command to continue from the checkpoint.
- Use `--no-resume` to ignore checkpoint files and restart from row 0.
- In dry-run mode, checkpoint files are based on the dry-run output path.

## Generate Sarcasm Labels With Pretrained Classifier

Use the helper script to classify each tweet in `dataset/election/data.csv` as sarcastic or not sarcastic using a local snapshot of `helinivan/english-sarcasm-detector`.

- Column written: `sarcasm_label`
- Label `0`: not sarcastic
- Label `1`: sarcastic
- Existing columns are preserved (no overwrite of `label` or `llm_label`).

Requires local model to be installed in model path; Install from: [https://huggingface.co/helinivan/english-sarcasm-detector/tree/main](https://huggingface.co/helinivan/english-sarcasm-detector/tree/main)
Run with a local model path:

```bash
python Scripts/sarcasm_detection_labels.py --model-path models/sarcasm_model
```

Dry-run on first N rows:

```bash
python Scripts/sarcasm_detection_labels.py --model-path models/sarcasm_model --dry-run --limit 200
```

Checkpoint and cache behavior:

- Periodic checkpoint files are written next to the selected output path.
- Re-run the same command to resume after interruption.
- Duplicate tweets are cached by normalized text to avoid repeated inference work.
- If inference fails for a row, the script leaves existing `sarcasm_label` unchanged.
- Startup diagnostics report model metadata and checkpoint loading stats to help detect model compatibility issues quickly.