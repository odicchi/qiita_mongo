from pymongo import MongoClient
from mongo_sample import MongoSample
import pprint

mongo = MongoSample('db', 'employee')

result = mongo.aggregate('Age')
print(type(result))
for doc in result:
    print(doc)