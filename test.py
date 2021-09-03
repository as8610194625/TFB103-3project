import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()
titlelist = []  #書名
htmls = []      #書本網址
images = []     #書本圖片
isbns = []      #ISBN
authors = []    #作家
publishs = []   #出版社
user_Agent = ua.random
# print(user_Agent)
headers = {
    'User-Agent': user_Agent
}
# for page in range(1, 5):
# url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/4/spell/3/ms2/ms2_1/key/python'
url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/spell/3/ms2/ms2_1/page/1/key/python'

# def get_titles(url):
res = requests.get(url, headers=headers)
# print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')
time.sleep(1)
titles = soup.select('table[id="itemlist_table"] img')
title_htmls_numbers = soup.select('table[id="itemlist_table"] tbody')
for html in title_htmls_numbers:
    html = "https://www.books.com.tw/products/"+(html['id'].split('_')[1])
    htmls.append(html)
    print(html)
print(len(htmls))
# for title in titles:
#     images.append(title['data-srcset'])#圖片網址
#     # print(title['data-srcset'])
#     titlelist.append(title['alt'])  #書名

    
