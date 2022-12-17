import datetime as dt
import pandas as pd

input_obj=pd.read_csv('data/' + 'kawamura'+ '01/' +'obj/'+ 'iraira1-1.csv',header=None)#ファイルの読み込み
first=(input_obj.head(1)).iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
#time=(first.split(' '))[1] #○○:○○:○○,○○○○
time2=dt.datetime.strptime(first,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
print("timestamp=",time2.timestamp()) #UNIX時間に



#time2=first+datetime.timedelta(seconds=30)
#print(time2)