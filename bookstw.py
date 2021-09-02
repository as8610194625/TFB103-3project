import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/1/spell/3/ms2/ms2_1/key/python"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,"html.parser")
print(soup)
