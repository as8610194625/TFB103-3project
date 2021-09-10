import requests
from bs4 import BeautifulSoup



headers = headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
page = 56
book_html = "https://www.kingstone.com.tw/search/key/java/page/{}".format(page)
book_res = requests.get(book_html,headers=headers)
book_soup = BeautifulSoup(book_res.text,"html.parser")
article = book_soup.select('h3[class="pdnamebox"] a')
# book_aurthor = book_soup.select('li[class="basicunit"] a')
# book_intro = book_soup.select('div[class="pdintro_txt1field panelCon"]')[0]
# print(book_aurthor[0],book_aurthor[3])
while not article ==[]:
    page +=1
    book_html = "https://www.kingstone.com.tw/search/key/java/page/{}".format(page)
    book_res = requests.get(book_html,headers=headers)
    book_soup = BeautifulSoup(book_res.text,"html.parser")
    article = book_soup.select('h3[class="pdnamebox"] a')
    # book_image = book_soup.select('div[class="alpha_main"] a')[0]['href']
    # isbn = book_soup.select('ul[class="table_2col_deda"]')[1].select('li[class="table_td"]')[1].text
    print(page)
    print('===')