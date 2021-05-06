import pymongo
from .check_statu import statu
from . import settings

class analysis():
    def __init__(self):
        self.myclient = pymongo.MongoClient(settings.MONGO_URL)

    def check_cookie(self):
        pass

    def get_Ch_id(self,Ch_name):
        pass

    def main(self,cookie,Ch_name,option):

        pass
