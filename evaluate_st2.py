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

def calc_readability(preds, refs):
  # Get readability scores
  fkgl_scores = []
  dcrs_scores = []

  for i, pred in enumerate(preds):
    fkgl_scores.append(np.abs(textstat.flesch_kincaid_grade(pred) - textstat.flesch_kincaid_grade(refs[i])))
    dcrs_scores.append(np.abs(textstat.dale_chall_readability_score(pred) - textstat.dale_chall_readability_score(refs[i])))
  
  return np.mean(fkgl_scores), np.mean(dcrs_scores)

def calc_bartscore(preds, srcs, sum_type):
  # Get BARTScore F1 scores
  bart_scorer = BARTScorer(device='cuda:0', max_length=8192, checkpoint=f'./models/bartscore/st2_{sum_type}')
  return np.mean(bart_scorer.score(srcs, preds))

def read_file_lines(path):
  with open(path, 'r') as f:
    lines = f.readlines()
  
  if path.endswith('.jsonl'):
    lines = [json.loads(line) for line in lines]
  return lines

def evaluate(pred_path, gold_path, sum_type):
  # Load data from files
  refs_dicts = read_file_lines(gold_path)
  preds = read_file_lines(pred_path)
  
  ref_str = "lay_summary" if sum_type == "laysumm" else "abstract"
  refs = [d[ref_str] for d in refs_dicts]
  docs = [d['article'] for d in refs_dicts]

  score_dict = {}

  # Relevance scores
  rouge1_score, rouge2_score, rougel_score = calc_rouge(preds, refs)
  score_dict['ROUGE1'] = rouge1_score
  score_dict['ROUGE2'] = rouge2_score
  score_dict['ROUGEL'] = rougel_score
  score_dict['BERTScore'] = calc_bertscore(preds, refs)

  # # Readability scores
  fkgl_score, dcrs_score = calc_readability(preds, refs)
  score_dict['FKGL'] = fkgl_score
  score_dict['DCRS'] = dcrs_score

  # # Factuality scores
  score_dict['BARTScore'] = calc_bartscore(preds, docs, sum_type)

  return score_dict

def write_scores(score_dict, output_filepath):
  # Write scores to file
  with open(output_filepath, 'w') as f:
    for key, value in score_dict.items():
      f.write(f"{key}: {value}\n")
      

submit_dir = sys.argv[1] # directory with txt files ("elife.txt" and "plos.txt") with predictions
truth_dir = sys.argv[2] # directory with jsonl files containing references and articles 
output_dir = "./"

# Calculate + write abstract scores
abstract_scores = evaluate(
  os.path.join(submit_dir, 'abstract.txt'), 
  os.path.join(truth_dir, 'val.jsonl'),
  "abstract"
  )
write_scores(abstract_scores, os.path.join(output_dir, 'st2_abstract_scores.txt'))

# Calculate + write laysumm scores
laysumm_scores = evaluate(
  os.path.join(submit_dir, 'laysumm.txt'), 
  os.path.join(truth_dir, 'val.jsonl'),
  "laysumm"
  )
write_scores(laysumm_scores, os.path.join(output_dir, 'st2_laysumm_scores.txt'))

# Calculate + write overall scores
avg_scores = {key: np.mean([abstract_scores[key], laysumm_scores[key]]) for key in abstract_scores.keys()}
write_scores(avg_scores, os.path.join(output_dir, 'st2_scores.txt'))