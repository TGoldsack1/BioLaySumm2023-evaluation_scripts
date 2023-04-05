# BioLaySumm Evaluation Scripts

This repository contains the scripts used to for evaluation for each subtask in the BioLaySumm 2023 Shared Task.


The scripts are configured to run on the validation data provided to participants.
***
## Setup

Before running the scripts, you must first install the dependencies. The easiest way to do this is to use the provided `requirements.txt` file.

```
pip install -r requirements.txt
```

Additionally, the checkpoints used for BARTScore will need to be downloaded. This can be done by running `get_models.sh` script:

```
bash ./get_models.sh
```

## Running Evaluation
Once setup is complete, you can run the evaluation scripts on your predicted summaries for each subtask. `evaluate_st1.py` and `evaluate_st2.py` are used to evaluate the summaries for subtask 1 and 2, respectively. The scripts expect 2 positional arguments: the path to the directory containing the predicted summary text files (i.e., `elife.txt` and `plos.txt` for subtask 1, or `abstract.txt` and `laysumm.txt` for subtask 2) and the path to directory containing provided validation `.jsonl` files. Example

```
evaluate_st1.py /path/to/predicted/summaries /path/to/validation/data
```

**Note** - running evaluation will take a long time without the use of a GPU. If your GPU doesn't have enough memory to run BARTScore, you can try reducing the batch size in `bartscore.py` or the `max_length` argument provided to BARTScore in the respective evaluation scripts. 