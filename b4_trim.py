import pandas as pd
import datetime as dt
from decimal import *

someone = ['tamura','suzuki']#,'shigenawa','maeda','kobayasi','kawasaki','watanabe','tamaru','nomura','motoyama','ota','kawamura','imahashi','yashiro','tabata']
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2']#'puzzle5-1','puzzle5-2','iraira5-1','iraira5-2',
day = ['01', '02']
df=pd.DataFrame(columns=file_name)
for sm in someone:
    for dy in day:
        l_sm=[]
        for fn in file_name:
            ################csvファイルから必要な時間の抽出#################
            input_obj=pd.read_csv('exp_data/' + sm+ dy +'/'+sm+dy+'_obj/'+ fn+'.csv',header=None)#ファイルの読み込み

            start=input_obj.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
            start_dt=dt.datetime.strptime(start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
            start_unix=start_dt.timestamp() #UNIX時間に

            end=input_obj.iloc[-1,0]
            end_dt=dt.datetime.strptime(end,'%Y-%m-%d %H:%M:%S.%f')
            end_unix=end_dt.timestamp() #UNIX時間に
            passtime=end_dt-start_dt
            print(passtime)
            l_sm.append(passtime)
            ##############################################################
        print(l_sm)
        df.loc[sm+dy]=l_sm
        """
        newline=pd.DataFrame([l_sm],columns=file_name,name=sm+dy)
        pd.concat([df,newline])
        """

df.to_csv('test.csv')