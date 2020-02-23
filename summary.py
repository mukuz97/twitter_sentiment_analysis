from pymongo import MongoClient

mongoClient = MongoClient()
db = mongoClient.tweets

WORD_SCPACE = 12

def formatNum(num):
    num = str(int(num))
    result = ''
    for i, s in enumerate(num[::-1]):
        result += s
        if (i+1)%3 == 0 and i < len(num) - 1:
            result += ','
    return result[::-1]

print('Subject',' '*5,'Tweets',' '*6,'Total Size')

for collection in db.list_collection_names():
    coll_stats = db.command("collstats", collection)
    print(
        collection,
        ' '*(WORD_SCPACE - len(collection)),
        formatNum(coll_stats['count']),
        ' '*(WORD_SCPACE - len(formatNum(coll_stats['count']))),
        formatNum(coll_stats['size']), 'Bytes'
    )

db_stats = db.command("dbstats")
print()
print('Total Tweets: ', formatNum(db_stats['objects']))
print('Total Size: ', formatNum(db_stats['dataSize']), 'Bytes')
print('Note: The actual file size in file system will be smaller due to compression')