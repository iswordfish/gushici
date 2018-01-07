import pymongo

class SaveSpider():
    """
    保存到mongoDB
    """
    def __init__(self,host,port,dbname,table):
        self.client = pymongo.MongoClient(host=host,port=port)

        self.mdb = self.client[dbname]
        self.table = self.mdb[table]

    def content_insert(self,item):
        data = item
        self.table.insert(data)

if __name__=="__main__":
    m = SaveSpider('127.0.0.1',27017,dbname ,authortable)
    m.content_insert(item)



