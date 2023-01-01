import pandas as pd
import datetime as dt
from decimal import *

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','motoyama','nomura','ota','shigenawa','suzuki','tabata','tamaru','watanabe','yashiro']#'tamura'
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
day = ['01', '02']
for sm in someone:
    for dy in day:
        l_sm=[]
        for fn in file_name:
            input_data=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv',index_col=None)#ファイルの読み込み
            
            start=input_data.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
            start_dt=dt.datetime.strptime(start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
            end=input_data.iloc[-1,0]
            end_dt=dt.datetime.strptime(end,'%Y-%m-%d %H:%M:%S.%f')
            passtime=end_dt-start_dt
            l_sm.append(passtime)
            
            print(sm+dy+":",end='')
            print(passtime)
            
        df.loc[sm+dy]=l_sm#被験者smのdy日目の時間をデータフレームに追加
        
df.to_csv('test.csv')#時間の情報をcsvに