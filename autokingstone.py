import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from fake_useragent import UserAgent


keywords = ['ega', 'egb', 'egc', 'egd', 'ege', 'egf', 'egg', 'egz', 'eha', 'ehb', 'ehc', 'ehd', 'ehe', 'ehf', 'ehg', 'ehh', 'ehi', 'ehj', 'ehz', 'eaa', 'eab', 'eac', 'ead',
'eae', 'eaf', 'eba', 'ebb', 'ebc', 'ebd', 'ebe', 'ebf', 'ebg', 'ebh', 'ebz', 'eca', 'ecb', 'ecc', 'ecd', 'ece', 'ecz', 'eda', 'edb', 'edc', 'edd', 'efa', 'efb', 'efc', 'efd',
'efe', 'eff', 'efg', 'efh', 'efi', 'efj', 'efz', 'eea', 'eeb', 'eec', 'eed', 'eee', 'eef', 'eeg', 'eeh', 'eei', 'eia', 'eib', 'eic', 'eid', 'eie', 'eif', 'eig', 'eih', 'eii',
'eij', 'eik', 'eil', 'eim', 'ein', 'eio', 'ezz', 'bea', 'bef', 'beg', 'beh', 'beb', 'bec', 'bed', 'bee', 'bei', 'bej', 'bda', 'bdo', 'bdc', 'bdf', 'bdg', 'bdh', 'bdi', 'bdj',
'bdk', 'bdl', 'bdm', 'bdn', 'bdb', 'bde', 'bdd', 'baa', 'bac', 'baj', 'bai', 'bab', 'baf', 'bag', 'bah', 'bad', 'bak', 'bal', 'bcb', 'bca', 'bcc', 'bcg', 'bcf', 'bce', 'bcd',
'bba', 'bbc', 'bbd', 'bbb', 'bbe', 'bbf', 'bzz', 'hda', 'hdf', 'hdg', 'hdi', 'hdh', 'hdd', 'hdb', 'hdc', 'hde', 'hgg', 'hge', 'hgf', 'hgl', 'hgd', 'hga', 'hgj', 'hgh', 'hgc',
'hgi', 'hgb', 'hgk', 'hca', 'hcb', 'hcc', 'hcd', 'hce', 'hcf', 'hcg', 'hkb', 'hkf', 'hke', 'hkd', 'hkc', 'hka', 'hld', 'hlc', 'hlb', 'hla', 'hli', 'hlg', 'hlh', 'hlf', 'hle',
'hmb', 'hmd', 'hme', 'hmc', 'hma', 'hmf', 'hfa', 'hfb', 'hfc', 'hfd', 'hfe', 'hfh', 'hfk', 'hfg', 'hfi', 'hff', 'hfo', 'hfm', 'hfj', 'hfl', 'hfn', 'hfp', 'hfq', 'hfz', 'hhf',
'hhd', 'hhe', 'hhc', 'hhb', 'hha', 'hhz', 'hea', 'hed', 'heb', 'hec', 'hee', 'hab', 'hac', 'haa', 'hba', 'hbb', 'hbc', 'hbf', 'hbe', 'hbd', 'hia', 'hif', 'hie', 'hic', 'hib',
'hid', 'hig', 'hiz', 'hja', 'hjb', 'hjc', 'hjz', 'hzz', 'iaa', 'iab', 'ika', 'ikb', 'ikc', 'ikd', 'ikz', 'ila', 'ilb', 'ilc', 'ild', 'ile', 'ilf', 'ilz', 'ima', 'imb', 'imc',
'imd', 'ime', 'imf', 'img', 'imh', 'imi', 'imz', 'ioa', 'iob', 'ioc', 'iod', 'ioe', 'iof', 'iog', 'ioh', 'ioi', 'ioj', 'iok', 'iol', 'iom', 'ion', 'ioo', 'iop', 'ioq', 'ior',
'ios', 'ioz', 'ica', 'icb', 'icc', 'icd', 'ice', 'icf', 'icg', 'ich', 'ici', 'icj', 'ick', 'icl', 'icm', 'ico', 'icz', 'iba', 'ibb', 'ibc', 'ibd', 'ibe', 'ibf', 'ibz', 'iea',
'ide', 'idc', 'idd', 'ida', 'idb', 'idf', 'idg', 'idh', 'idi', 'idz', 'ija', 'ijb', 'ijc', 'ijd', 'ije', 'ijf', 'ijg', 'ijh', 'iji', 'ijz', 'iia', 'iga', 'igb', 'igc', 'igd',
'iha', 'ihb', 'ihc', 'ihd', 'ifb', 'ifc', 'ifa', 'ifd', 'ife', 'ifz', 'ipa', 'iqa', 'iqb', 'iqc', 'iqd', 'iqe', 'iqf', 'iqg', 'iqp', 'iqh', 'iqi', 'iqj', 'iqk', 'iql', 'iqm',
'iqn', 'iqo', 'iqz', 'ssz', 'taa', 'tab', 'tac', 'tae', 'taf', 'tag', 'tah', 'tai', 'tak', 'tal', 'tam', 'tan', 'tao', 'taq', 'tar', 'tas', 'tat', 'tau', 'taw', 'tax', 'tba',
'tbb', 'tbc', 'tbe', 'tbf', 'tbg', 'tbh', 'tbi', 'tbk', 'tbl', 'tbm', 'tbn', 'tbo', 'tbq', 'tbr', 'tbs', 'tbt', 'tbu', 'tbw', 'tbx', 'tca', 'tcb', 'tcc', 'tce', 'tcf', 'tcg',
'tch', 'tci', 'tck', 'tcl', 'tcm', 'tcn', 'tco', 'tcq', 'tcr', 'tcs', 'tct', 'tcu', 'tcw', 'tcx', 'tcy', 'tcz', 'tc1', 'tc3', 'tc4', 'tda', 'tdb', 'tdc', 'tde', 'tdf', 'tdg',
'tdh', 'tdi', 'tdk', 'tdl', 'tdm', 'tdn', 'tdo', 'tdq', 'tdr', 'tds', 'tdt', 'tdu', 'tdw', 'tdx', 'tdy', 'tdz', 'td1', 'td3', 'td4', 'tea', 'teb', 'tec', 'tee', 'tef', 'teg',
'teh', 'tei', 'tek', 'tel', 'tem', 'ten', 'teo', 'teq', 'ter', 'tes', 'tet', 'teu', 'tew', 'tex', 'tey', 'tez', 'te1', 'te3', 'te4', 'tfa', 'tfb', 'tfc', 'tfe', 'tff', 'tfg',
'tfh', 'tfi', 'tfk', 'tfl', 'tfm', 'tfn', 'tfo', 'tfq', 'tfr', 'tfs', 'tft', 'tfu', 'tfw', 'tfx', 'tfy', 'tfz', 'tf1', 'tf3', 'tf4', 'tga', 'tgb', 'tgc', 'tgd', 'tha', 'thb',
'thc', 'thd', 'the', 'thf', 'thg', 'thh', 'thi', 'thj', 'thk', 'thl', 'thm', 'thn', 'tho', 'thp', 'thq', 'thr', 'ths', 'tht', 'tia', 'tib', 'tic', 'tid', 'tie', 'tif', 'tig',
'tih', 'tii', 'tij', 'tik', 'til', 'tim', 'tin', 'tio', 'tip', 'tiq', 'tir', 'tis', 'tit', 'tja', 'tjb', 'tjc', 'tjd', 'tje', 'tjf', 'tjg', 'tjh', 'tji', 'tjj', 'tjk', 'tjl',
'tjm', 'tjn', 'tjo', 'tjp', 'tjq', 'tjr', 'tjs', 'tjt', 'tka', 'tkb', 'tkc', 'tkd', 'tke', 'tkf', 'tkg', 'tkh', 'tki', 'tkj', 'tkk', 'tkl', 'tkm', 'tkn', 'tko', 'tkp', 'tkq',
'tkr', 'tks', 'tkt', 'tku', 'tla', 'tlb', 'tlc', 'tld', 'tle', 'tlf', 'tlg', 'tlh', 'tli', 'tlj', 'tlk', 'tll', 'tlm', 'tln', 'tlo', 'tlp', 'tlq', 'tlr', 'tls', 'tlt', 'tlu',
'tma', 'tmb', 'tmc', 'tmd', 'tme', 'tmf', 'tmg', 'tmh', 'tmi', 'tmj', 'tna', 'tnb', 'tnc', 'tnd', 'tne', 'tnf', 'tng', 'tnh', 'tni', 'tnj', 'toa', 'tob', 'toc', 'tod', 'toe',
'tof', 'tog', 'toh', 'toi', 'toj', 'tpa', 'tpb', 'tpc', 'tpd', 'tpe', 'tpf', 'tpg', 'tph', 'tpi', 'tpj', 'tqa', 'tqb', 'tqc', 'tqd', 'tqe', 'tqf', 'tqg', 'tqh', 'tqi', 'tqj',
'tra', 'trb', 'trc', 'trd', 'tre', 'trf', 'trg', 'trh', 'tri', 'trj', 'tsa', 'tsb', 'tsc', 'tsd', 'tse', 'tsf', 'tsg', 'tsh', 'tsi', 'tsj', 'tsk', 'tzz']
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
    if soup.select('div[class="txtregion_resultno"]') == []:
        df = pd.DataFrame(data=book_np,columns=["書名","書籍網站","作者","出版社","ISBN","圖片網址"])
        df_intro = pd.DataFrame(data=book_intro_np,columns=["ISBN","書籍簡介"])
        df.to_csv("./kingstone_datas/books/kingstone_{}.csv".format(keyword),encoding="utf-8-sig",index=False)
        df_intro.to_csv("./kingstone_datas/intros/kingstone_{}_intro.csv".format(keyword),encoding="utf-8-sig",index=False)
        print("Completed")
    time.sleep(5)

    # time.sleep(90)


input("Press Enter to exit!")

