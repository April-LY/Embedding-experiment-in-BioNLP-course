# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 15/05/2021 20:09
@Author: yao
"""

import os
import json

from collections import defaultdict
from nltk import sent_tokenize, word_tokenize
from string import punctuation
#from src.config import paras

def extract_text(file_path: str, save_file: str, token_fre_file: str, token_fre_low_file: str):

    token_fre_dict = defaultdict(int)
    # fixme: test
    save_count = 0
    wf = open(save_file, 'w', encoding='utf-8')
    text = ''

    with open(file_path) as f:
        doc = f.readlines()
    for line in doc:
        line = line.split("\t")
        text += str(line)
    
    for sentence in sent_tokenize(text):
        save_count += 1
        token_list = [token for token in word_tokenize(sentence) if token not in punctuation]
        wf_line = '\t'.join(token_list)
        wf.write(f'{wf_line}\n')
            
        for token in token_list:
            token_fre_dict[token] += 1
    wf.close()

    writed_token = set()
    token_sorted = sorted(token_fre_dict, key=lambda x: token_fre_dict[x], reverse=True)
    wf_low = open(token_fre_low_file, 'w', encoding='utf-8')
    with open(token_fre_file, 'w', encoding='utf-8') as wf:
        for token in token_sorted:
            wf.write(f'{token}\t{token_fre_dict[token]}\n')
            if token.lower() not in writed_token:
                writed_token.add(token.lower())
                token_count = token_fre_dict[token] + token_fre_dict[token.lower()] if token_fre_dict.get(token.lower()) else token_fre_dict[token]
                wf_low.write(f'{token.lower()}\t{token_count}\n')
    wf_low.close()
    print(f'{save_file}, {token_fre_file} save done, {save_count:,} sentences.')

if __name__ == '__main__':
    data_path = '../data/reference_PMID.match.table.txt'
    #json_data_path = 'data/litcovid-data/litcovid_AGAC_only'
    sentence_save_file = '../data/rto.sentence.txt'
    token_count_file = '../data/rto.TokenFrequency.txt'
    token_low_count_file = '../data/rto.TokenFrequency.low.txt'
    extract_text(data_path, sentence_save_file, token_count_file, token_low_count_file)
