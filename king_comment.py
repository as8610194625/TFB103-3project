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
    crawlered=list(map(lambda x : x[8:11],files))
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

categories=['ega', 'egb', 'egc', 'egd', 'ege', 'egf', 'egg', 'egz', 'eha', 'ehb', 'ehc', 'ehd', 'ehe', 'ehf', 'ehg', 'ehh', 'ehi', 'ehj', 'ehz', 'eaa', 
            'eab', 'eac', 'ead', 'eae', 'eaf', 'eba', 'ebb', 'ebc', 'ebd', 'ebe', 'ebf', 'ebg', 'ebh', 'ebz', 'eca', 'ecb', 'ecc', 'ecd', 'ece', 'ecz', 
            'eda', 'edb', 'edc', 'edd', 'efa', 'efb', 'efc', 'efd', 'efe', 'eff', 'efg', 'efh', 'efi', 'efj', 'efz', 'eea', 'eeb', 'eec', 'eed', 'eee', 
            'eef', 'eeg', 'eeh', 'eei', 'eia', 'eib', 'eic', 'eid', 'eie', 'eif', 'eig', 'eih', 'eii', 'eij', 'eik', 'eil', 'eim', 'ein', 'eio', 'ezz', 
            'bea', 'bef', 'beg', 'beh', 'beb', 'bec', 'bed', 'bee', 'bei', 'bej', 'bda', 'bdo', 'bdc', 'bdf', 'bdg', 'bdh', 'bdi', 'bdj', 'bdk', 'bdl', 
            'bdm', 'bdn', 'bdb', 'bde', 'bdd', 'baa', 'bac', 'baj', 'bai', 'bab', 'baf', 'bag', 'bah', 'bad', 'bak', 'bal', 'bcb', 'bca', 'bcc', 'bcg', 
            'bcf', 'bce', 'bcd', 'bba', 'bbc', 'bbd', 'bbb', 'bbe', 'bbf', 'bzz', 'hda', 'hdf', 'hdg', 'hdi', 'hdh', 'hdd', 'hdb', 'hdc', 'hde', 'hgg', 
            'hge', 'hgf', 'hgl', 'hgd', 'hga', 'hgj', 'hgh', 'hgc', 'hgi', 'hgb', 'hgk', 'hca', 'hcb', 'hcc', 'hcd', 'hce', 'hcf', 'hcg', 'hkb', 'hkf', 
            'hke', 'hkd', 'hkc', 'hka', 'hld', 'hlc', 'hlb', 'hla', 'hli', 'hlg', 'hlh', 'hlf', 'hle', 'hmb', 'hmd', 'hme', 'hmc', 'hma', 'hmf', 'hfa', 
            'hfb', 'hfc', 'hfd', 'hfe', 'hfh', 'hfk', 'hfg', 'hfi', 'hff', 'hfo', 'hfm', 'hfj', 'hfl', 'hfn', 'hfp', 'hfq', 'hfz', 'hhf', 'hhd', 'hhe', 
            'hhc', 'hhb', 'hha', 'hhz', 'hea', 'hed', 'heb', 'hec', 'hee', 'hab', 'hac', 'haa', 'hba', 'hbb', 'hbc', 'hbf', 'hbe', 'hbd', 'hia', 'hif', 
            'hie', 'hic', 'hib', 'hid', 'hig', 'hiz', 'hja', 'hjb', 'hjc', 'hjz', 'hzz', 'iaa', 'iab', 'ika', 'ikb', 'ikc', 'ikd', 'ikz', 'ila', 'ilb', 
            'ilc', 'ild', 'ile', 'ilf', 'ilz', 'ima', 'imb', 'imc', 'imd', 'ime', 'imf', 'img', 'imh', 'imi', 'imz', 'ioa', 'iob', 'ioc', 'iod', 'ioe', 
            'iof', 'iog', 'ioh', 'ioi', 'ioj', 'iok', 'iol', 'iom', 'ion', 'ioo', 'iop', 'ioq', 'ior', 'ios', 'ioz', 'ica', 'icb', 'icc', 'icd', 'ice', 
            'icf', 'icg', 'ich', 'ici', 'icj', 'ick', 'icl', 'icm', 'ico', 'icz', 'iba', 'ibb', 'ibc', 'ibd', 'ibe', 'ibf', 'ibz', 'iea', 'ide', 'idc', 
            'idd', 'ida', 'idb', 'idf', 'idg', 'idh', 'idi', 'idz', 'ija', 'ijb', 'ijc', 'ijd', 'ije', 'ijf', 'ijg', 'ijh', 'iji', 'ijz', 'iia', 'iga', 
            'igb', 'igc', 'igd', 'iha', 'ihb', 'ihc', 'ihd', 'ifb', 'ifc', 'ifa', 'ifd', 'ife', 'ifz', 'ipa', 'iqa', 'iqb', 'iqc', 'iqd', 'iqe', 'iqf', 
            'iqg', 'iqp', 'iqh', 'iqi', 'iqj', 'iqk', 'iql', 'iqm', 'iqn', 'iqo', 'iqz', 'ssz', 'taa', 'tab', 'tac', 'tae', 'taf', 'tag', 'tah', 'tai', 
            'tak', 'tal', 'tam', 'tan', 'tao', 'taq', 'tar', 'tas', 'tat', 'tau', 'taw', 'tax', 'tba', 'tbb', 'tbc', 'tbe', 'tbf', 'tbg', 'tbh', 'tbi', 
            'tbk', 'tbl', 'tbm', 'tbn', 'tbo', 'tbq', 'tbr', 'tbs', 'tbt', 'tbu', 'tbw', 'tbx', 'tca', 'tcb', 'tcc', 'tce', 'tcf', 'tcg', 'tch', 'tci', 
            'tck', 'tcl', 'tcm', 'tcn', 'tco', 'tcq', 'tcr', 'tcs', 'tct', 'tcu', 'tcw', 'tcx', 'tcy', 'tcz', 'tc1', 'tc3', 'tc4', 'tda', 'tdb', 'tdc', 
            'tde', 'tdf', 'tdg', 'tdh', 'tdi', 'tdk', 'tdl', 'tdm', 'tdn', 'tdo', 'tdq', 'tdr', 'tds', 'tdt', 'tdu', 'tdw', 'tdx', 'tdy', 'tdz', 'td1', 
            'td3', 'td4', 'tea', 'teb', 'tec', 'tee', 'tef', 'teg', 'teh', 'tei', 'tek', 'tel', 'tem', 'ten', 'teo', 'teq', 'ter', 'tes', 'tet', 'teu', 
            'tew', 'tex', 'tey', 'tez', 'te1', 'te3', 'te4', 'tfa', 'tfb', 'tfc', 'tfe', 'tff', 'tfg', 'tfh', 'tfi', 'tfk', 'tfl', 'tfm', 'tfn', 'tfo', 
            'tfq', 'tfr', 'tfs', 'tft', 'tfu', 'tfw', 'tfx', 'tfy', 'tfz', 'tf1', 'tf3', 'tf4', 'tga', 'tgb', 'tgc', 'tgd', 'tha', 'thb', 'thc', 'thd', 
            'the', 'thf', 'thg', 'thh', 'thi', 'thj', 'thk', 'thl', 'thm', 'thn', 'tho', 'thp', 'thq', 'thr', 'ths', 'tht', 'tia', 'tib', 'tic', 'tid', 
            'tie', 'tif', 'tig', 'tih', 'tii', 'tij', 'tik', 'til', 'tim', 'tin', 'tio', 'tip', 'tiq', 'tir', 'tis', 'tit', 'tja', 'tjb', 'tjc', 'tjd', 
            'tje', 'tjf', 'tjg', 'tjh', 'tji', 'tjj', 'tjk', 'tjl', 'tjm', 'tjn', 'tjo', 'tjp', 'tjq', 'tjr', 'tjs', 'tjt', 'tka', 'tkb', 'tkc', 'tkd', 
            'tke', 'tkf', 'tkg', 'tkh', 'tki', 'tkj', 'tkk', 'tkl', 'tkm', 'tkn', 'tko', 'tkp', 'tkq', 'tkr', 'tks', 'tkt', 'tku', 'tla', 'tlb', 'tlc', 
            'tld', 'tle', 'tlf', 'tlg', 'tlh', 'tli', 'tlj', 'tlk', 'tll', 'tlm', 'tln', 'tlo', 'tlp', 'tlq', 'tlr', 'tls', 'tlt', 'tlu', 'tma', 'tmb', 
            'tmc', 'tmd', 'tme', 'tmf', 'tmg', 'tmh', 'tmi', 'tmj', 'tna', 'tnb', 'tnc', 'tnd', 'tne', 'tnf', 'tng', 'tnh', 'tni', 'tnj', 'toa', 'tob', 
            'toc', 'tod', 'toe', 'tof', 'tog', 'toh', 'toi', 'toj', 'tpa', 'tpb', 'tpc', 'tpd', 'tpe', 'tpf', 'tpg', 'tph', 'tpi', 'tpj', 'tqa', 'tqb', 
            'tqc', 'tqd', 'tqe', 'tqf', 'tqg', 'tqh', 'tqi', 'tqj', 'tra', 'trb', 'trc', 'trd', 'tre', 'trf', 'trg', 'trh', 'tri', 'trj', 'tsa', 'tsb', 
            'tsc', 'tsd', 'tse', 'tsf', 'tsg', 'tsh', 'tsi', 'tsj', 'tsk', 'tzz'] 

crawler(categories)
