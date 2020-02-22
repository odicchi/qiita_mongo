from mongo_sample import MongoSample
import pprint
# arg1:DB Name
# arg2:Collection Name
mongo = MongoSample("db", "qiita")

# 合計値
pipeline = [
    {"$group":{ "_id":"sum","page_max_view":{"$sum":"$page_views_count"}}}
]
results = mongo.aggregate(pipeline)
pprint.pprint(list(results))

# 最大値
pipeline = [
    {"$group":{ "_id":"title","page_max_view":{"$max":"$page_views_count"}}}
]
results = mongo.aggregate(pipeline)
pprint.pprint(list(results))

# 最小値
pipeline = [
    {"$group":{ "_id":"title","page_min_view":{"$min":"$page_views_count"}}}
]
results = mongo.aggregate(pipeline)
pprint.pprint(list(results))

# 平均値
pipeline = [
    {"$group":{ "_id":"average","page_average_view":{"$avg":"$page_views_count"}}}
]
results = mongo.aggregate(pipeline)
pprint.pprint(list(results))

# tag毎の出現回数カウント
pipeline = [
    { "$unwind": "$tag_list"}, 
    { "$group": { "_id": "$tag_list", "count": { "$sum":1}}},
    { "$sort": {"count": -1, "_id":1}}
]

results = mongo.aggregate(pipeline)
pprint.pprint(list(results))
