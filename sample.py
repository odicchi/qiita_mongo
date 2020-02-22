from get_qiita_info import GetQiitaInfo
from mongo_sample import MongoSample

# Qiitaの記事情報を取得する
qiita = GetQiitaInfo()
items = qiita.get_items()

# arg1:DB Name
# arg2:Collection Name
mongo = MongoSample("db", "qiita")
mongo.delete_many({})
# 不要なキー値を削除しないのであれば
# mongo.insert_many(items)
# で一括登録

for item in items:
    # rendered_body/body は不要なので削除
    item.pop("rendered_body")
    item.pop("body")
    # 一件ずつ登録
    mongo.insert_one(item)

result = mongo.find_one()
print(result)
