import pymysql
import pandas as pd
import os
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

for filename in os.listdir(os.getcwd()+'\\kingstone_datas\\books'):
    get_data(os.getcwd()+'\\kingstone_datas\\books\\'+filename)
    print(filename)
# def main():
#     # 讀取資料
#     get_data('kingstone_C.csv')

# if __name__ == '__main__':
#     main()


# for f in *.csv
# do
# winpty mysql -u root -p -e "LOAD DATA LOCAL INFILE  '"$f"' INTO TABLE books CHARACTER SET UTF8 FIELDS TERMINATED BY ',' ENCLOSED BY '""' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
# done