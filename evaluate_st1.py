import os, sys, json

import textstat
import numpy as np
from rouge_score import rouge_scorer
from bert_score import score
from bart_score import BARTScorer
import nltk 

nltk.download('punkt')

def calc_rouge(preds, refs):
  # Get ROUGE F1 scores
  scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeLsum'], use_stemmer=True, split_summaries=True)
  scores = [scorer.score(p, refs[i]) for i, p in enumerate(preds)]
  return np.mean([s['rouge1'].fmeasure for s in scores]), \
         np.mean([s['rouge2'].fmeasure for s in scores]), \
         np.mean([s['rougeLsum'].fmeasure for s in scores])

def calc_bertscore(preds, refs):
  # Get BERTScore F1 scores
  P, R, F1 = score(preds, refs, lang="en", verbose=True, device='cuda:0')
  return np.mean(F1.tolist())

def calc_readability(preds):
  # Get readability scores
  fkgl_scores = []
  dcrs_scores = []
  for pred in preds:
    fkgl_scores.append(textstat.flesch_kincaid_grade(pred))
    dcrs_scores.append(textstat.dale_chall_readability_score(pred))
  return np.mean(fkgl_scores), np.mean(dcrs_scores)


def calc_bartscore(preds, srcs, ds):
  # Get BARTScore scores
  bart_scorer = BARTScorer(device='cuda:0', max_length=8192, checkpoint=f'./models/bartscore/st1_{ds}')
  return np.mean(bart_scorer.score(srcs, preds))

def read_file_lines(path):
  with open(path, 'r') as f:
    lines = f.readlines()
  
  if path.endswith('.jsonl'):
    lines = [json.loads(line) for line in lines]
  return lines

def evaluate(pred_path, gold_path, ds):
  # Load data from files
  refs_dicts = read_file_lines(gold_path)
  preds = read_file_lines(pred_path)
  
  refs = [d['lay_summary'] for d in refs_dicts]
  docs = [d['article'] for d in refs_dicts]

  score_dict = {}

  # Relevance scores
  rouge1_score, rouge2_score, rougel_score = calc_rouge(preds, refs)
  score_dict['ROUGE1'] = rouge1_score
  score_dict['ROUGE2'] = rouge2_score
  score_dict['ROUGEL'] = rougel_score
  score_dict['BERTScore'] = calc_bertscore(preds, refs)

  # # Readability scores
  fkgl_score, dcrs_score = calc_readability(preds)
  score_dict['FKGL'] = fkgl_score
  score_dict['DCRS'] = dcrs_score

  # Factuality scores
  score_dict['BARTScore'] = calc_bartscore(preds, docs, ds)

  return score_dict

def write_scores(score_dict, output_filepath):
  # Write scores to file
  with open(output_filepath, 'w') as f:
    for key, value in score_dict.items():
      f.write(f"{key}: {value}\n")


submit_dir = sys.argv[1] # directory with txt files ("elife.txt" and "plos.txt") with predictions
truth_dir = sys.argv[2] # directory with jsonl files containing references and articles 

output_dir = "./"

# Calculate + write eLife scores
elife_scores = evaluate(
  os.path.join(submit_dir, 'elife.txt'), 
  os.path.join(truth_dir, 'eLife_val.jsonl'),
  "elife"
  )
write_scores(elife_scores, os.path.join(output_dir, 'st1_elife_scores.txt'))

# Calculate + write PLOS scores
plos_scores = evaluate(
  os.path.join(submit_dir, 'plos.txt'), 
  os.path.join(truth_dir, 'PLOS_val.jsonl'),
  "plos"
  )
write_scores(plos_scores, os.path.join(output_dir, 'st1_plos_scores.txt'))

# Calculate + write overall scores
avg_scores = {key: np.mean([elife_scores[key], plos_scores[key]]) for key in elife_scores.keys()}
write_scores(avg_scores, os.path.join(output_dir, 'st1_scores.txt'))