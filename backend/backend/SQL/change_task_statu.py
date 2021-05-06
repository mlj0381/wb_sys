from .base_sql import Basic_opear as sql

class change_statu(object):

    def begin(self,Ch_name):
        sql().update('ch_info', 'ch_info', {'Ch_name': Ch_name}, {'statu': 1})

    def pause(self,Ch_name):
        sql().update('ch_info','ch_info',{'Ch_name':Ch_name},{'statu':0})

    def deldata(self,Ch_name):
        sql().update('ch_info', 'ch_info', {'Ch_name': Ch_name}, {'statu': -1})

    def main(self,Ch_name,statu):
        statu = int(statu)
        if(statu==1):
            self.begin(Ch_name)
        elif(statu == 0):
            print("6666")
            self.pause(Ch_name)
        else:
            self.deldata(Ch_name)


