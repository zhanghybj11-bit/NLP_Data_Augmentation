"""
@Time : 2025/6/6
@Auth : zhanghy
@DESCRIPTION: 采用EDA的方法来实现文本的数据增强
"""

import jieba
import http.client
import hashlib
import urllib
import random
import json
import time
from utils.utils import write_samples
import os
from eda import *

def aug_continue(sample_path, translate_path):
    try:
        import csv
        with open(sample_path, 'r', encoding='utf8') as in_file, \
            open(translate_path, 'w', encoding='utf-8', newline='') as out_file:
            line_count = 0  # 行号计数器
            reader = csv.DictReader(in_file)
            writer = csv.writer(out_file)
            # next(reader)
            headers = ['ID', 'label', 'review999']
            writer.writerow(headers)

            for row in reader:
                if int(row['ID']) >= 0:  # 检查指定列的值 9,97,54
                    print(row)

                    # eda--------start---------
                    aug_sentences = eda(row['review'], alpha_sr=0.05, alpha_ri=0.05, alpha_rs=0.05, p_rd=0.05, num_aug=4)
                    print(aug_sentences)
                    for aug_sentence in aug_sentences:
                        writer.writerow([row['ID'], row['label'],aug_sentence.replace(" ", "")])
                    # eda--------end---------

                    if int(row['ID']) == 13:  # 检查指定列的值
                        print(f"到目标行 {3}，退出读取")
                        break
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

if __name__ == '__main__':

    from datetime import datetime
    now = datetime.now()
    time_str = now.strftime('%Y-%m-%d %H%M%S')
    
    sample_path = './data/file-test6.csv'
    data_path = f'./data/eda_file-test6_{time_str}.csv'
    aug_continue(sample_path, data_path)


    
