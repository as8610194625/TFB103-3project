import pymysql
import pandas as pd
import os
from multiprocessing import Process
def get_data(file_name):
    data = pd.read_csv(file_name,engine='python',encoding='utf-8')
    # print(data.head(3))

    conn = pymysql.connect(
        user = 'root',
        port = 3306,
        passwd = '0000',
        db = 'kingstone',
        host = 'localhost',
        charset = 'utf8mb4'
    )
    cursor = conn.cursor()
    data = data.astype(object).where(pd.notnull(data), None) 

    for bookname,bookhtml,author,publisher,isbn,imagehtml in zip(data['書名'],data['書籍網站'],data['作者'],data['出版社'],data['ISBN'],data['圖片網址']):

        dataList = [bookname,bookhtml,author,publisher,isbn,imagehtml]

        print (dataList) # 插入的值
        print('........')
        
        try:
            insertsql = "INSERT INTO books(書名,書籍網站,作者,出版社,ISBN,圖片網址) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(insertsql,dataList)
            conn.commit()
        except Exception as e:
            print ("Exception")
            print (e)
            conn.rollback()
            
    cursor.close()
    # 關閉資料庫連線
    conn.close()

def get_dataintro(file_name):
    data = pd.read_csv(file_name,engine='python',encoding='utf-8')
    # print(data.head(3))

    conn = pymysql.connect(
        user = 'root',
        port = 3306,
        passwd = '0000',
        db = 'kingstone',
        host = 'localhost',
        charset = 'utf8mb4'
    )
    cursor = conn.cursor()
    data = data.astype(object).where(pd.notnull(data), None) 

    for isbn,bookintro in zip(data['ISBN'],data['書籍簡介']):

        dataList = [isbn,bookintro]

        print (dataList) # 插入的值
        print('........')
        
        try:
            insertsql = "INSERT INTO books_intros(ISBN,書籍簡介) VALUES(%s,%s)"
            cursor.execute(insertsql,dataList)
            conn.commit()
        except Exception as e:
            print ("Exception")
            print (e)
            conn.rollback()
            
    cursor.close()
    # 關閉資料庫連線
    conn.close()
def data():
    for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\books'):
        get_data(os.getcwd()+'\\kingstone_datas\\books\\'+filename)
        print(filename)
def data_intros():
    for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\intros'):
        get_dataintro(os.getcwd()+'\\kingstone_datas\\intros\\'+filename)
        print(filename)
def main3():
    p1 = Process(target=data)
    p1.start()

    p2 = Process(target=data_intros)
    
    p2.start()

# def main():
#     # 讀取資料
#     get_data('kingstone_C.csv')

if __name__ == '__main__':
    main3()