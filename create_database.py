from pymongo import MongoClient
import datetime

# mongodb へのアクセスを確立
client = MongoClient('localhost', 27017)

# データベースを作成 (名前: my_database)
db = client['db']

# コレクションを作成 (名前: my_collection)
co = db['employee']


post = {"Name": "Matsui",
        "age": 26}

result1 = co.insert_one(post)