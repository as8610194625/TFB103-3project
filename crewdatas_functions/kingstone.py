import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
def kingstone(keyword,pages):
    book =list()
    bookhtml =list()
    bookauthor =list()
    bookpublisher = list()
    imagehtml = list()
    isbn = list()
    book_intros = list()
    for page in range (1,int(pages)+1):
        url = "https://www.kingstone.com.tw/search/key/{}/page/{}".format(keyword,str(page))
        headers = headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,"html.parser")
        article = soup.select('h3[class="pdnamebox"] a')
        
        for k,i in enumerate (article):
            # book_name = i.text
            book.append(i.text)
            book_html = "https://www.kingstone.com.tw/"+i['href']
            bookhtml.append(book_html)
            book_res = requests.get(book_html,headers=headers)
            time.sleep(1)
            book_soup = BeautifulSoup(book_res.text,"html.parser")
            bookauthor.append(book_soup.select('li[class="basicunit"] a')[0].text)
            if book_soup.select('li[class="basicunit"] a')[2].text == '?':
                bookpublisher.append(book_soup.select('li[class="basicunit"] a')[3].text)
            else:
                bookpublisher.append(book_soup.select('li[class="basicunit"] a')[2].text)
            imagehtml.append(book_soup.select('div[class="alpha_main"] a')[0]['href'])
            try:
                isbn.append(book_soup.select('ul[class="table_2col_deda"]')[1].select('li[class="table_td"]')[1].text)
            except IndexError:
                isbn.append(0)
            try:
                book_intro = book_soup.select('div[class="pdintro_txt1field panelCon"]')[0]
                book_intros.append(book_intro.text)
            except IndexError:
                book_intros.append(0)
            
            print(k+1,i.text)
            print("Loading.....")
            time.sleep(3)
        time.sleep(5)
        print("第{}頁".format(page).center(20,"="))
    # print(len(book))
    # print(len(bookhtml))
    # print(len(bookauthor))
    # print(len(bookpublisher))
    # print(len(isbn))
    # print(len(imagehtml))
    data ={
        "書名":book,
        "書籍網址":bookhtml,
        "作者":bookauthor,
        "出版社":bookpublisher,
        "ISBN":isbn,
        "圖片網址":imagehtml
    }
    data_intro ={
        "ISBN":isbn,
        "書籍簡介":book_intros
    }
    
    df = pd.DataFrame(data=data)
    df_intro = pd.DataFrame(data=data_intro)
    df.to_csv("kingstone_{}.csv".format(keyword),encoding="utf-8-sig",index=False)
    df_intro.to_csv("kingstone_{}_intro.csv".format(keyword),encoding="utf-8-sig",index=False)
    print("Completed")
    
kingstone(input("您要搜尋的書籍?"),input("您要總查詢的頁數?"))
input("Press Enter to exit!")