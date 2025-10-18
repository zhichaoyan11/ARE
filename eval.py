import json
import re
import os
import spacy
import math
from tqdm import tqdm
import Levenshtein
from evalution_attr import auto_ais_edit, auto_ais_edit_rarr
spacy_model = spacy.load("en_core_web_sm")
import nltk
from nltk.translate.bleu_score import sentence_bleu


def kg_aug_evaluate(filename):
    result_file = filename
    with open(result_file, 'r') as rf:

        evidence_ori_claim_ais_score = 0.0
        evidence_new_claim_ais_score = 0.0
        total_pres = 0.0
        evidence_new_claim_ais_score_sub_fact = 0.0
        lines = rf.readlines()
        score_dict = {}
        before_scores = []
        after_scores = []
        after_scores_sub_fact = []
        before_noise_ais_scores = []
        before_bleu_scores = []
        after_bleu_scores = []
        after_bleu_score_result = 0.0
        after_noise_ais_scores = []
        after_noise_ais_scores_sub_fact = []
        after_af1_scores = []
        before_binary_results = 0
        after_binary_results = 0

        for line in tqdm(lines):

            json_data = json.loads(line)
            ori_answer = json_data['input_info']['predict_answer']
            question = json_data['ori_question']
            gold_answer = json_data['gold_answer']
            ori_claim = json_data['RARR_result']['revisions'][0]['original_text']
            # ori_claim = json_data['RARR_result']['questions']
            revised_text = json_data['RARR_result']['revisions'][0]['revised_text']
            
            # ARE的计算方式
            revised_text_with_sub_fact = json_data['RARR_result']['revisions'][0]['sub_fact_revised']
            total_pres += preservation(ori_claim, revised_text_with_sub_fact)
            

            
            used_evidence = []
            total_evidence = json_data['RARR_result']['revisions'][0]['evidences']
            # evidence中的text是原始的evidence，sub_fact_evidences是可能重新进行检索后的evidence
            
            # # ARE的计算方式
            total_evidence = [[v for v in item["sub_fact_evidences"].values()] for item in total_evidence]
            for k in range(len(total_evidence)):
                used_evidence.append(
                    ''.join(remove_dup(".".join(total_evidence[k])))
                    )
           
            
            before_score, before_noise_ais_score, before_binary_result, before_bleu_score = 0,0,0,0
            if math.isnan(before_noise_ais_score):
                continue
            before_af1 = 2*before_score*(1-before_noise_ais_score) / (before_score+(1-before_noise_ais_score))
            before_binary_results += before_binary_result
            before_noise_ais_scores.append(before_noise_ais_score)
            before_scores.append(before_score)
            before_bleu_scores.append(before_bleu_score)
            
            after_score, after_noise_ais_score, after_binary_result, after_bleu_score = 0,0,0,0
            after_score_sub_fact, after_noise_ais_score_sub_fact, after_binary_result, _ = auto_ais_edit(revised_text_with_sub_fact, used_evidence,question, spacy_model)
            if after_noise_ais_score_sub_fact == 1.0:
                print("11111")
            after_binary_results += after_binary_result
            
            after_scores.append(after_score)
            after_scores_sub_fact.append(after_score_sub_fact)
            after_bleu_scores.append(after_bleu_score)
            after_bleu_score_result += after_bleu_score
            after_noise_ais_scores.append(after_noise_ais_score)
            after_noise_ais_scores_sub_fact.append(after_noise_ais_score_sub_fact)
            evidence_ori_claim_ais_score += before_score
            evidence_new_claim_ais_score += after_score
            evidence_new_claim_ais_score_sub_fact += after_score_sub_fact
            af1 = 2*after_score*(1-after_noise_ais_score) / (after_score+(1-after_noise_ais_score))
            sub_fact_af1 = 2*after_score_sub_fact*(1-after_noise_ais_score_sub_fact) / (after_score_sub_fact+(1-after_noise_ais_score_sub_fact))
            after_af1_scores.append(af1)
            score_dict[question] = [af1, sub_fact_af1]
        before_af1 = (2*(1-sum(before_noise_ais_scores) / len(lines))*(evidence_ori_claim_ais_score / len(lines))) / ((1-sum(before_noise_ais_scores) / len(lines))+(evidence_ori_claim_ais_score / len(lines)))
        f1 = (2*(1-sum(after_noise_ais_scores) / len(lines))*(evidence_new_claim_ais_score / len(lines))) / ((1-sum(after_noise_ais_scores) / len(lines))+(evidence_new_claim_ais_score / len(lines)))
        bp = 1-(sum(before_noise_ais_scores) / len(lines))
        ap = 1-(sum(after_noise_ais_scores)) / len(lines)
        br = evidence_ori_claim_ais_score / len(lines)
        ar = evidence_new_claim_ais_score / len(lines)
        b_af1 = before_af1
        a_af1 = f1
        bbr = before_binary_results/len(lines)
        abr = after_binary_results/len(lines)
        pres = total_pres/len(lines)
        f1_arp  = 2*ar*pres/(ar+pres)
        return bp,ap,br,ar,b_af1,a_af1,bbr,abr,pres,f1_arp