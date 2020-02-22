from pymongo import MongoClient
from MongoSample import MongoSample

mongo = MongoSample('db', 'employee')

find = mongo.find()
print('-------------------find-------------------')
print(type(find))
for doc in find:
    print(doc)

mongo.insert_one({'name':'Oshima','Age':21})

find = mongo.find()
print('-------------------find-------------------')
print(type(find))
for doc in find:
    print(doc)
