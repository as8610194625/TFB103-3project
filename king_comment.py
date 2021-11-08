import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import time
import json

def crawler(categories):

    if not os.path.exists('./book_comment'):
        os.mkdir('./book_comment')

    files=os.listdir('book_comment')
    crawlered=list(map(lambda x : x[0:3],files))
    categories=list(set(crawlered) ^ set(categories))

    for category in categories:
        book_info=[]
        kurl = "https://www.kingstone.com.tw/book/{}/".format(category)
        page=1
        while True:

            us = UserAgent()
            user_agent = us.random
            headers = {'User-Agent': user_agent}
       
            try:
                try:
                    url = kurl+"?&page={}".format(str(page))                
                    res = requests.get(url,headers=headers)
                except:
                    url = kurl+"page/{}".format(str(page))                        
                    res = requests.get(url,headers=headers)
                soup = BeautifulSoup(res.text,"html.parser")
                articleurl = soup.select('h3[class="pdnamebox"] a')
                print(category,'第',page,'頁，共',len(articleurl),'則')

            except:
                print('!! Request Denied ~~~~~~~~~~~~~~~~~~~~~~ ')
                time.sleep(120)
                try:
                    url = kurl+"?&page={}".format(str(page))                
                    res = requests.get(url,headers=headers)
                except:
                    url = kurl+"page/{}".format(str(page))                        
                    res = requests.get(url,headers=headers)
                finally:
                    articleurl = soup.select('h3[class="pdnamebox"] a')

            finally:
                if len(articleurl)==0:
                    print('Anti Crawler is shown. Sleep for 120 s')
                    time.sleep(120)
                    res = requests.get(url,headers=headers)
                    soup = BeautifulSoup(res.text,"html.parser")
                    articleurl = soup.select('h3[class="pdnamebox"] a')

            for i in articleurl:
                title = i.text
                book_html = "https://www.kingstone.com.tw/"+i['href']
                try:
                    time.sleep(1)
                    book_dict={}
                    ua = UserAgent()
                    user_agent = ua.random
                    headers = {'User-Agent': user_agent}
                    book_res = requests.get(book_html,headers=headers)
                    book_soup = BeautifulSoup(book_res.text,"html.parser")

                    try:
                        isbn = book_soup.select('li[class="table_td"]')[3].text
                        single_comment=book_soup.select('ul[class="comment1col"] li')
                        if single_comment==[]:
                            print('no comment')
                        else:
                            for single in single_comment:
                                user=single.select('span[class="name_cmt1"]')[0].text.split('說')[0].strip()
                                print(user)
                                comment=single.select('div[class="td_comment1"]')[0].text.strip()
                                print(comment)
                                time.sleep(1)
                                book_dict['BOOKNAME']=title
                                book_dict['ISBN']=isbn
                                book_dict['USER']=user
                                book_dict['CONTENT']=comment
                                book_info.append(book_dict)
                    except:
                        isbn = 0
                        print('no isbn')

                except IndexError as a:
                    print(title,' with ',a)
                    continue
                
                except:
                    print('other error')
                    time.sleep(120)
                    continue
                    
            if soup.select('li[class="pageNext"]')==[]:
                break
            else:
                page+=1
                time.sleep(1)

        with open('./book_comment/comment_%s.json'%(category),'w',encoding='utf-8') as f:
            json.dump(book_info,f,ensure_ascii=False)

categories=['qjz','ddd', 'cee', 'cge', 'dge', 'dez', 'ceg', 'dga', 'gbm', 'gbn', 'djz', 'qac', 'gbs', 'dbc', 'cgc', 'dcc',
         'qee', 'dbb', 'qie', 'gee', 'ccd', 'dlb', 'dcb', 'cec',
         'dhh', 'ggd', 'cca', 'qfe', 'ddc', 'gbf', 'geb', 'qjb', 'dfz', 'dhi',
         'cba', 'gaz', 'gbt', 'dgc', 'qcg', 'dib', 'dcd', 'caa', 'qjc', 'gbr',
         'qha', 'cfd', 'qcj', 'dja', 'gbd', 'qcb', 'gbl', 'qad', 'qga', 'ccc', 'qeg', 'djb', 'geg', 'qib', 'gbz',
         'cfb', 'qfg', 'cbc', 'gfb', 'deg', 'dbe', 'gfh', 'ddz', 'dba', 'dec', 'gdh', 'dkc', 'cej', 'dig', 'gej',
         'dzz', 'cdz', 'gaa', 'gdg', 'deh', 'qgb', 'qaf', 'qia', 'qfc', 'qkc', 'qef', 'ged', 'qbc', 'gde',
         'gbu', 'qfa', 'dif', 'gcb', 'dhc', 'gbb', 'cgg', 'qik', 'dka',
         'qed', 'deb', 'qeb', 'del', 'ghc', 'gda', 'qid', 'qcd', 'dce', 'geh', 'gei', 'dea', 'qdb', 'ghf', 'qka', 'qig', 'qdf', 'gbe',
         'qab', 'gfe', 'qkb', 'cea', 'dbz', 'ghd', 'qch', 'cbd', 'qff', 'gbi', 'ceb', 'ggc', 'dla', 'dei', 'ghe', 'dlz', 'cfa',
         'qbz', 'qla', 'gae', 'qcf', 'gbg', 'qae', 'cgd', 'dda', 'dfb', 'die', 'dic', 'qaa', 'qcc', 'cdb', 'gga', 'cdc', 'gdc', 'gac', 'qca',
         'dbd', 'dle', 'gfc', 'gdd', 'dca', 'cbb', 'cga', 'qfd', 'qij', 'dhb',
         'gbv', 'ded', 'gba', 'qea', 'dfa', 'dem', 'gbx', 'cab', 'gfd', 'qag',
         'cda', 'gfg', 'dkb', 'qdc', 'qhc', 'dhd', 'cff', 'gdi', 'diz', 'ccb',
         'dhz', 'dgb', 'qfh', 'gab', 'dgd', 'qke', 'cel', 'dcz', 'gef', 'gbh',
         'gbj', 'dia', 'cac', 'cgb', 'cad', 'gdf', 'gfa', 'did', 'gbo', 'ghg',
         'cfc', 'gff', 'dhe', 'qck', 'dhf', 'gbc', 'ced', 'dej', 'gbp', 'dlc',
         'qde', 'dek', 'gbw', 'dha', 'gea', 'qif', 'gca', 'gha', 'qbd', 'gbq',
         'cef', 'qih', 'dee', 'dld', 'qkd', 'ghb', 'qda', 'dgf', 'qce', 'qhb', 'cek', 'gdj', 'qfb', 'qja', 'cfe',
         'qic', 'qii', 'dab', 'gzz', 'qdd', 'daa', 'cei', 'qjd', 'qld',
         'gbk', 'dhg', 'qec', 'def', 'qci', 'czz', 'qba', 'gec', 'qbb', 'cgf', 'ggb', 'gad', 'gdb', 'ceh']

crawler(categories)
