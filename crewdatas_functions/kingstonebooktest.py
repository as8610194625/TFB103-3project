import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from fake_useragent import UserAgent

li = list()
ua = UserAgent()
user_agent = ua.random
keywords = ['dddd','oooo','pppp','jjjj','uuuu']
def key(keyword):

    kurl = "https://www.kingstone.com.tw/book/{}/".format(keyword)
    headers = {'User-Agent': user_agent}
    res = requests.get(kurl,headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    article = soup.select('nav[class="navcolumn_classlevel"]')[0].select('a[class=""]')
    # print(article)
    for a in article:
        li.append(a.get('href').split('/')[-1])
    return li
a = map(key,keywords)
aaaa =list(a)[-1]
# print(li)
ll = []
def kkkkkey(keyword):
    kurl = "https://www.kingstone.com.tw/book/{}/".format(keyword)
    headers = {'User-Agent': user_agent}
    res = requests.get(kurl,headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    article = soup.select('nav[class="navcolumn_classlevel"]')[0].select('a[class=""]')
    # print(article)
    for a in article:
        aa = (a.get('href').split('/')[-1])
        if len(aa) == 3:
            ll.append(aa)
    return ll
b = map(kkkkkey,aaaa)
bbbb = list(b)[-1]
print(ll)