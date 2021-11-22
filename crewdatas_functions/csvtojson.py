from json import encoder
import pandas as pd
import json
import os 

# file = './test.json'
# filename = (open(file,'r',encoding='utf-8'))
# for line in filename.readlines():
#     js = json.loads(line)
#     print(js)

# def csvtojson(file):
#     cv = pd.read_csv('kingstone_datas\\books\\'+file,encoding='utf8')
#     js = cv.to_json('.\\json\\books\\'+file.split('.csv')[0]+'.json',orient = 'records',lines=True, force_ascii=False)
# def csvtojson2(file):
#     cv = pd.read_csv('kingstone_datas\\intros\\'+file,encoding='utf8')
#     js = cv.to_json('.\\json\\intros\\'+file.split('.csv')[0]+'.json',orient = 'records',lines=True, force_ascii=False)


# for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\books'):
#         csvtojson(filename)
#         print(filename)
# for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\intros'):
#         csvtojson2(filename)
#         print(filename)

def merge(filename,filename2):
    cv = pd.read_csv('kingstone_datas\\books\\'+filename,encoding='utf8')
    cvintro = pd.read_csv('kingstone_datas\\intros\\'+filename2,encoding='utf8')
    cv2 = cv.merge(cvintro['書籍簡介'],how='left',left_index=True,right_index=True)
    cv2.to_csv('kingstone_datas\\merge_datas\\'+filename,encoding='utf-8-sig',index=False)
    js = cv2.to_json('json\\'+filename.split('.csv')[0]+'.json',orient = 'records',lines=True, force_ascii=False)
    print('ok')


for filename,filename2 in zip(os.listdir(os.getcwd()+'\\kingstone_datas\\books'),os.listdir(os.getcwd()+'\\kingstone_datas\\intros')):
    merge(filename,filename2)
print('COMPLETED')
