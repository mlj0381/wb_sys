#该函数为了求后几天日期用

#参数(array[年,月，日,求后几天的日期])

class reckon():
    def __init__(self):
        pass
    
    def year(self,x):
        return (0 if x%4 else 1) if x % 100 else 1

    def mon(self,x):
        return (28 if x == 2 else ( 31 if x in [1,3,5,7,8,10,12] else 30))

    def one_day(self,x):
        if(x[2]-1==0):
            if(x[1]-1==0):
                years = x[0] -1
                mons = 12
                days = 31
            else:
                years = x[0]
                mons = x[1]-1
                days = self.mon(mons)
                if(self.year(years) and mons ==2):
                    days += 1
        else:
            years = x[0]
            mons = x[1]
            days = x[2]-1

        return ([years,mons,days])

    def main(self,array):
        x = array[0].split('-')
        for i in range(len(x)):
            try:
                x[i]=int(x[i])
            except:
                x[i] = int(x[i]-'00')
        times=[[x[0],x[1],x[2]]]

        print(x)
        for i in range(array[1]-1):
            times.append(self.one_day(times[len(times)-1]))
        for i in range(len(times)):
            if (times[i][1] < 10):
                times[i][1] = '0' + str(times[i][1])
            if (times[i][2] < 10):
                times[i][2] = '0' + str(times[i][2])
            times[i] = str(times[i][0]) + '-' + str(times[i][1]) + '-' + str(times[i][2])
        return times
