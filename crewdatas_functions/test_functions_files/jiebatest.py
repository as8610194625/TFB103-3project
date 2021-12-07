import json
import jieba
import re
# jieba.set_dictionary('dict.txt.big')
jieba.case_sensitive = True
counts = {}
for article in open (r"./kingstone_datas/json/kingstone_baa.json",'r',encoding='utf-8-sig'):
    words = json.loads(article)['書籍簡介'].replace('\r','').replace('\n','')
    words = ''.join(re.findall(u'[\u4e00-\u9fa5]+',words))
    words = jieba.cut(words)
    # print(list(words))
    for word in words:
        counts[word] = counts.get(word,0)+1
items=list(counts.items())
# print(items)
items.sort(key=lambda x:x[1],reverse=True)
for i in range(len(items)):
    word,count=items[i]
    if count > 5:
        print(word,count)
