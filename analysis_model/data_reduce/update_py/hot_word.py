import pymongo
import jieba
import re
from . import settings
#按时间分类
#返回前20热词
#不足20返回尽量多

class hot_words(object):
    def __init__(self):
        myclient = pymongo.MongoClient(settings.MONGO_URL)
        db =  myclient['spider']
        self.table = db['iniv_content_0405']


    def hot_words(self,times,Ch_id):
        counts = {}
        for time in times:
            for id in Ch_id:
                recode = self.table.find({"Ch_id": id, "iniv_date": re.compile(time)},{"iniv_content_text": 1})
                sentence = ""
                for i in recode:
                    sentence = sentence + i['iniv_content_text']

                v = []
                with open("./update_py/word_type/废词.txt", "r", encoding="utf-8") as t:
                    for i in t:
                        v.append(i.strip())

                for word in jieba.lcut(sentence):
                    if(word not in v and word != '\xa0' and word != "️"):
                        counts[word] = counts.get(word,0)+1
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        array=[]
        number = len(items)
        for i in range(20):
            if(i  ==number):
                break
            array.append(list(items[i]))
        return array

    def main(self,times,Ch_id=False):
        return self.hot_words(times,Ch_id)
