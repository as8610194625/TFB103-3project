import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://cdn.kingstone.com.tw/english/images/product/8726/9783030188726.jpg"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,"html.parser")
# article = soup.select
print(soup)