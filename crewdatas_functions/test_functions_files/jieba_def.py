import jieba
import re

jieba.case_sensitive = True
def cut_words(article):
    words = article.replace('\r','').replace('\n','')
    words = ''.join(re.findall(u'[\u4e00-\u9fa5]+',words))
    words = jieba.cut(words)
    # print(list(words))
    return list(words)
