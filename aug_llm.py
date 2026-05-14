"""
@Time : 2025/6/6
@Auth : zhanghy
@DESCRIPTION: 采用大模型的方法来实现文本的数据增强
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
from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.1.99:11434/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def llm_continue(sample_path, translate_path):
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
                    print(row['review'])
                    # 原句子写入
                    print(row['ID'], row['label'],row['review'])
                    writer.writerow([row['ID'], row['label'],row['review']])

                    #第一次调用 qwen2.5:latest+++++++++++
                    ret_sent1 = augmentation_from_model("qwen2.5:latest", row['review'])
                    writer.writerow([row['ID'], row['label'], ret_sent1])
                    #第二次调用 qwen2.5:latest
                    ret_sent2 = augmentation_from_model("qwen2.5:latest", row['review'])
                    writer.writerow([row['ID'], row['label'], ret_sent2])
                    
                    #第一次调用 lm4:9b-------------------------
                    ret_sent11 = augmentation_from_model("glm4:9b", row['review'])
                    writer.writerow([row['ID'], row['label'], ret_sent11])
                    #第二次调用 lm4:9b
                    ret_sent12 = augmentation_from_model("glm4:9b", row['review'])
                    writer.writerow([row['ID'], row['label'], ret_sent12])

                    if int(row['ID']) == 130:  # 检查指定列的值
                        print(f"到目标行 {3}，退出读取")
                        break
    except Exception as e:
        print(f"处理过程中发生错误：{e}")



def augmentation_from_model(model_name, sentence):
    chat_response = client.chat.completions.create(
        # model="qwen2.5:latest",
        # model="glm4:9b",
        model=model_name,
        messages=[
            {"role": "system", "content": 
            "你是建筑工程方面的专家，请仿写下面的句子。要求仅给出仿写后的句子，无需其他内容；尽量避免使用原句中的词语；面积偏差不能超过百分之十；施工类型类似但不相同。"},
            {"role": "user", "content": sentence
            #"Tell me something about large language models."
            },
        ],
        temperature=1,
        top_p=1,
        max_tokens=512,
        extra_body={
            "repetition_penalty": 1.2,
        },
    )
    ret_sent = chat_response.choices[0].message.content
    print("Chat response:", ret_sent)
    return ret_sent


if __name__ == '__main__':

    from datetime import datetime
    now = datetime.now()
    time_str = now.strftime('%Y-%m-%d %H%M%S')

    sample_path = './data/file-test6.csv'
    data_path = f'./data/llm_file-test6.csv_{time_str}'
    llm_continue(sample_path, data_path)
