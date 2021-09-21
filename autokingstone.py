import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from fake_useragent import UserAgent


keywords = ['taq', 'tar', 'tas', 'tat', 'tau', 'taw', 'tax', 'tba','tbb', 'tbc', 'tbe', 'tbf', 'tbg', 'tbh', 'tbi', 'tbk', 'tbl', 'tbm', 'tbn', 'tbo', 'tbq', 'tbr', 'tbs', 'tbt', 'tbu', 'tbw', 'tbx', 'tca', 'tcb', 'tcc', 'tce', 'tcf', 'tcg',
'tch', 'tci', 'tck', 'tcl', 'tcm', 'tcn', 'tco', 'tcq', 'tcr', 'tcs', 'tct', 'tcu', 'tcw', 'tcx', 'tcy', 'tcz', 'tc1', 'tc3', 'tc4', 'tda', 'tdb', 'tdc', 'tde', 'tdf', 'tdg',
'tdh', 'tdi', 'tdk', 'tdl', 'tdm', 'tdn', 'tdo', 'tdq', 'tdr', 'tds', 'tdt', 'tdu', 'tdw', 'tdx', 'tdy', 'tdz', 'td1', 'td3', 'td4', 'tea', 'teb', 'tec', 'tee', 'tef', 'teg',
'teh', 'tei', 'tek', 'tel', 'tem', 'ten', 'teo', 'teq', 'ter', 'tes', 'tet', 'teu', 'tew', 'tex', 'tey', 'tez', 'te1', 'te3', 'te4', 'tfa', 'tfb', 'tfc', 'tfe', 'tff', 'tfg',
'tfh', 'tfi', 'tfk', 'tfl', 'tfm', 'tfn', 'tfo', 'tfq', 'tfr', 'tfs', 'tft', 'tfu', 'tfw', 'tfx', 'tfy', 'tfz', 'tf1', 'tf3', 'tf4', 'tga', 'tgb', 'tgc', 'tgd', 'tha', 'thb',
'thc', 'thd', 'the', 'thf', 'thg', 'thh', 'thi', 'thj', 'thk', 'thl', 'thm', 'thn', 'tho', 'thp', 'thq', 'thr', 'ths', 'tht', 'tia', 'tib', 'tic', 'tid', 'tie', 'tif', 'tig',
'tih', 'tii', 'tij', 'tik', 'til', 'tim', 'tin', 'tio', 'tip', 'tiq', 'tir', 'tis', 'tit', 'tja', 'tjb', 'tjc', 'tjd', 'tje', 'tjf', 'tjg', 'tjh', 'tji', 'tjj', 'tjk', 'tjl',
'tjm', 'tjn', 'tjo', 'tjp', 'tjq', 'tjr', 'tjs', 'tjt', 'tka', 'tkb', 'tkc', 'tkd', 'tke', 'tkf', 'tkg', 'tkh', 'tki']
ua = UserAgent()
user_agent = ua.random
for keyword in keywords:
    kurl = "https://www.kingstone.com.tw/book/{}/".format(keyword)
    page = 0
    article = [0]
    book_np = 0
    while not article == [] :
        try:
            page += 1
            url = kurl+"?&page={}".format(str(page))
            headers = {'User-Agent': user_agent}
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            article = soup.select('h3[class="pdnamebox"] a')
        except:
            page += 1
            url = kurl+"page/{}".format(str(page))
            headers = {'User-Agent': user_agent}
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            article = soup.select('h3[class="pdnamebox"] a')
        if soup.select('div[class="txtregion_resultno"]') != []:
            break
        else:
            if article != []:
                for k,i in enumerate (article):
                    book = list()
                    book_intros = list()
                    # book_name = i.text
                    title = i.text
                    book_html = "https://www.kingstone.com.tw/"+i['href']
                    try:
                        book_res = requests.get(book_html,headers=headers)
                        time.sleep(1)
                    except:
                        continue
                    book_soup = BeautifulSoup(book_res.text,"html.parser")
                    try:
                        author = book_soup.select('li[class="basicunit"] a')[0].text #作者
                        if book_soup.select('li[class="basicunit"] a')[2].text == '?':
                            publisher = book_soup.select('li[class="basicunit"] a')[3].text #出版社
                        else:
                            publisher = book_soup.select('li[class="basicunit"] a')[2].text #出版社
                        imagehtml = book_soup.select('div[class="alpha_main"] a')[0]['href'] #圖片網址
                        try:
                            isbn = book_soup.select('ul[class="table_2col_deda"]')[1].select('li[class="table_td"]')[1].text #isbn
                        except IndexError:
                            isbn = 0
                        try:
                            book_intro = book_soup.select('div[class="pdintro_txt1field panelCon"]')[0].text
                        except IndexError:
                            book_intro = 0
                        book.extend([title,book_html,author,publisher,isbn,imagehtml])
                        book_intros.extend([isbn,book_intro])
                        if book_np is 0:
                            book_np = np.array([book])
                            book_intro_np = np.array([book_intros])
                        else:
                            book_np = np.vstack([book_np,book])
                            book_intro_np = np.vstack([book_intro_np,book_intros])
                    except:
                        continue
                    print(k+1,i.text)
                    print("Loading.....")
                    # time.sleep(3)
                
                print("第{}頁".format(page).center(20,"="))
                time.sleep(5)
            else:
                print("OKOKOK")
                break
    if soup.select('div[class="txtregion_resultno"]') == [] and book_np != 0 :
        df = pd.DataFrame(data=book_np,columns=["書名","書籍網站","作者","出版社","ISBN","圖片網址"])
        df_intro = pd.DataFrame(data=book_intro_np,columns=["ISBN","書籍簡介"])
        df.to_csv("./kingstone_datas/books/kingstone_{}.csv".format(keyword),encoding="utf-8-sig",index=False)
        df_intro.to_csv("./kingstone_datas/intros/kingstone_{}_intro.csv".format(keyword),encoding="utf-8-sig",index=False)
        print("Completed")
    time.sleep(5)

    # time.sleep(90)


input("Press Enter to exit!")

