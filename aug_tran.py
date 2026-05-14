"""
@Time : 2025/6/6
@Auth : zhanghy
@File ：back_translate.py
@DESCRIPTION: 采用回译的方法来实现文本的数据增强
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

def translate(q, src_lang, tgt_lang):
    """请求百度通用翻译API，详细请看 https://api.fanyi.baidu.com/doc/21
    :param q:
    :param src_lang:
    :param tgt_lang:
    :return:
    """

    appid = '20250306002294404'  # Fill in your AppID
    secretKey = 'p8heLpQOWoNAKquzdUAT'  # Fill in your key

    httpClient = None
    myurl = '/api/trans/vip/translate'

    salt = random.randint(0, 4000)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = '/api/trans/vip/translate' + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + src_lang + '&to=' + tgt_lang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #print(myurl)
        # response is HTTPResponse object
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        #print(result)
        return result

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

def back_translate(q, src_lang="zh", tgt_lang="en"):
    """
    :param q: 文本
    :param src_lang: 原始语言
    :param tgt_lang: 目前语言
    :return: 回译后的文本
    """
    en = translate(q, src_lang, tgt_lang)['trans_result'][0]['dst']
    time.sleep(1.5)
    target = translate(en, tgt_lang, src_lang)['trans_result'][0]['dst']
    time.sleep(1.5)
    return target

def translate_continue(sample_path, translate_path):
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
                # if int(row['ID']) == 98:  # 检查指定列的值 1 99 98
                    print(row)
                    
                    # tran--------start---------
                    # 原句子写入
                    print(row['ID'], row['label'],row['review'])
                    # writer.writerow([row['ID'], row['label'],row['review']])
                    
                    # # 译文句子生成并写入en
                    # tran1 = back_translate(row['review'])
                    # writer.writerow([row['ID'], row['label'],tran1])
                    # # 译文句子生成并写入jp
                    # tran2 = back_translate(row['review'],"zh","jp")
                    # writer.writerow([row['ID'], row['label'],tran2])
                    # # 译文句子生成并写入kor
                    # tran4 = back_translate(row['review'],"zh","kor")
                    # writer.writerow([row['ID'], row['label'],tran4])
                    '''
                    # 译文句子生成并写入fra
                    tran3 = back_translate(row['review'],"zh","fra")
                    writer.writerow([row['ID'], row['label'],tran3])
                    #de
                    # tran5 = back_translate(row['review'],"zh","de")
                    # writer.writerow([row['ID'], row['label'],tran5])
                    #俄语ru 
                    tran6 = back_translate(row['review'],"zh","ru")
                    writer.writerow([row['ID'], row['label'],tran6])
                    '''
                    #西班牙语spa
                    tran7 = back_translate(row['review'],"zh","spa")
                    writer.writerow([row['ID'], row['label'],tran7])
                    print(tran7)
                    
                    if int(row['ID']) == 127:  # 检查指定列的值 127
                        print(f"到目标行 {3}，退出读取")
                        break
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

if __name__ == '__main__':

    from datetime import datetime
    now = datetime.now()
    time_str = now.strftime('%Y-%m-%d')

    sample_path = './data/file-test6.csv'
    tran_eda_path = f'./data/tran_file-test6_{time_str}.csv'
    translate_continue(sample_path, tran_eda_path)
