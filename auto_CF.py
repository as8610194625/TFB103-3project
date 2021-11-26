from pymongo import MongoClient, collection
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import statsmodels.api as sm

connection = MongoClient(host='localhost',port=27017)
db = connection.kingstone
collection = db['CFmodel']
datas = list(collection.find())
original_df = pd.DataFrame(datas)
del original_df['_id']
#清理空值及相同資料
original_df = original_df.dropna(axis=0)
duplicates = original_df.duplicated()
if duplicates.sum() > 0:
    print('> {} duplicates'.format(duplicates.sum()))
    rating_df = original_df[~duplicates]

print('> {} duplicates'.format(rating_df.duplicated().sum()))

# ISBN轉為字串 移除 ISBN等於 0
rating_df['ISBN'] = rating_df['ISBN'].astype('str')
rating_df=rating_df.drop(rating_df[rating_df["ISBN"]=='0'].index,axis=0) 
rating_df['USERSTAR'] = rating_df['USERSTAR'].astype('float')
rating_df['user_id'] = pd.Categorical(rating_df.USER).codes   
book_features_df = rating_df.pivot_table(index = 'ISBN',columns = 'user_id',values = 'USERSTAR')
#空值0取代
book_features_df.fillna(0, inplace = True)


# 稀疏矩陣

book_features_df_matrix = csr_matrix(book_features_df.values)

# 建立餘弦相似模型 (K-近鄰演算法)

nearest_neighbor_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
nearest_neighbor_model.fit(book_features_df_matrix)

# 建模及跑模型
my_dict = {}
for book_index in range(book_features_df.shape[0]):
    
    one_dimensional_representation_of_book_vector = book_features_df.iloc[book_index].values.reshape(1, -1)
    distances, indices = nearest_neighbor_model.kneighbors(one_dimensional_representation_of_book_vector, n_neighbors = 4)
    indices = indices.flatten()
    distances = distances.flatten()
    similar_books = []
    
    for i in range(0, len(indices)):
        ## same book
        if i == 0:
            original_book = book_features_df.index[book_index]
        else:
            ## similar books
            similar_books.append(book_features_df.index[indices[i]])

        my_dict[original_book] = similar_books

# 存入資料庫
coll = db['userCF']
coll.drop()
for isbn,lists in my_dict.items():
    data={"ISBN":isbn,"list":lists}
#     print(kv)
    coll.insert([data])
