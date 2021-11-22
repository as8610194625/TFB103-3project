import requests
from bs4 import BeautifulSoup

url = "https://www.eslite.com/Search?keyword=python&final_price=0%2C&sort=_weight_+desc&size=20&start=0"
headers = headers = {'Referer':'https://www.eslite.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,"html.parser")
print(soup)
