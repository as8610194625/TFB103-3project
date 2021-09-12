import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from fake_useragent import UserAgent

keywords = [
    'DeepLearning','深度學習',
    'Machine Learning','機器學習','TensorFlow','影像辨識','Image-recognition','語音辨識',
    'Speech-recognition','Computer Vision','電腦視覺','Reinforcement','強化學習','Web API Design',
    'WebAssembly','Ext JS','TypeScript','React','Golang','Laravel','Ruby','Django','Node.js','Flask',
    'Linux','Qt Command line','Vim','BSD','Apple Developer','Android','Cross-Platform','Hack','Penetration-test',
    'Wireshark','Fintech','Blockchain','Amazon Web Services','DevOps','Kubernetes','Microsoft Azure'
]
# keywords = [
#     'NoSQL','MySQL','Oracle','MongoDB','Elasticsearch','PostgreSQL',
#     'Python','C','C++','Java','JavaScript','PHP','R語言','Text-mining',
#     '文字探勘','Data-visualization','資料視覺化','ETL網路爬蟲','Data-mining',
#     '資料探勘','HTML','CSS','Bootstrap','Ajax','jQuery','DeepLearning','深度學習',
#     'Machine Learning','機器學習','TensorFlow','影像辨識','Image-recognition','語音辨識',
#     'Speech-recognition','Computer Vision','電腦視覺','Reinforcement','強化學習','Web API Design',
#     'WebAssembly','Ext JS','TypeScript','React','Golang','Laravel','Ruby','Django','Node.js','Flask',
#     'Linux','Qt Command line','Vim','BSD','Apple Developer','Android','Cross-Platform','Hack','Penetration-test',
#     'Wireshark','Fintech','Blockchain','Amazon Web Services','DevOps','Kubernetes','Microsoft Azure','Docker','虛擬化技術',
#     'Virtualization','OpenStack','Google Cloud','Game-engine','3D-modeling','Game-design','VR/AR','OpenGL','WebGL','Computer-Science',
#     '計算機概論','Operating-system','作業系統原理','資料結構與演算法','Information-management','資訊管理','Computer-architecture','計算機組織',
#     'Compiler','編譯器','Computer-networks','TCP/IP','HTTP','Wireless-networks','Mobile-communication','Communication-systems','Wi-Fi','LTE','AutoCAD',
#     'Artlantis','Catia','CNS','Fusion 360','Mastercam','Photograph','Digital-image','Powerdirector','Videostudio','Illustrator','Design Pattern','Object-oriented',
#     '物件導向','Refactoring','Domain-DrivenDesign','Access','Excel','Word','PowerPoint'
# ]
ua = UserAgent()
user_agent = ua.random
for keyword in keywords:   
    kurl = "https://www.kingstone.com.tw/search/key/{}/cl/自然科普_電腦資訊_考試書／政府出版品/".format(keyword)
    page = 0
    article = [0]
    book_np = 0
    while not article == [] :
        try:
            page += 1
            url = kurl+"page/{}".format(str(page))
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
                    book =list()
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
                time.sleep(9)
            else:
                print("OKOKOK")
                break
    if soup.select('div[class="txtregion_resultno"]') == []:
        df = pd.DataFrame(data=book_np,columns=("書名","書籍網站","作者","出版社","ISBN","圖片網址"))
        df_intro = pd.DataFrame(data=book_intro_np,columns=("ISBN","書籍簡介"))
        df.to_csv("kingstone_{}.csv".format(keyword),encoding="utf-8-sig",index=False)
        df_intro.to_csv("kingstone_{}_intro.csv".format(keyword),encoding="utf-8-sig",index=False)
        print("Completed")
    # time.sleep(5)

    # time.sleep(90)


input("Press Enter to exit!")

