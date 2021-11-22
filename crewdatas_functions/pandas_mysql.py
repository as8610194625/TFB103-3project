import pymysql
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('root','0000','localhost','kingstone','utf8mb4'), )
data = pd.read_json(r'C:\Users\Tibame\kingstonedatas.json',lines=True)
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
data.to_sql(name='cleanbooks',con=engine,if_exists='append',index=False)
sql = "SELECT * FROM `cleanbooks`"
cursor.execute(sql)
cursor.close()
conn.close()
# cursor = conn.cursor()
# data = data.astype(object).where(pd.notnull(data), None) 

# for bookname,bookhtml,author,publisher,isbn,imagehtml in zip(data['書名'],data['書籍網站'],data['作者'],data['出版社'],data['ISBN'],data['圖片網址'],data['書籍簡介']):

#     dataList = [bookname,bookhtml,author,publisher,isbn,imagehtml]

#     print (dataList) # 插入的值
#     print('........')
    
#     try:
#         insertsql = "INSERT INTO books(書名,書籍網站,作者,出版社,ISBN,圖片網址,書籍簡介) VALUES(%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(insertsql,dataList)
#         conn.commit()
#     except Exception as e:
#         print ("Exception")
#         print (e)
#         conn.rollback()
        
# cursor.close()
# # 關閉資料庫連線
# conn.close()