import pandas as pd
import datetime as dt
from decimal import *

someone = ['tamura']#''imahashi',,'kawamura''kawasaki','kobayashi','maeda','motoyama','nomura','ota','shigenawa','suzuki','tabata','tamaru','watanabe','yashiro',,
file_name = ['puzzle5-1','puzzle5-2','iraira5-1','iraira5-2']#',,,'n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2'
day = ['02']#,,,'02'
for sm in someone:
    for dy in day:
        l_sm=[]
        for fn in file_name:            
            ###############################アイトラッカーデータ#############################
            input_mouse=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv', index_col=None)#マウスデータ読み込み
            
            for i in range(len(input_mouse)):#時間の書き換え
                t_stamp=input_mouse.iloc[i,0]
                start_dt=dt.datetime.strptime(t_stamp,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
                start_unix=start_dt.timestamp() #UNIX時間に
                input_mouse.iloc[i,0]=start_unix
            input_mouse.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv',  index=False)#ファイルに出力

            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv', index_col=None)#マウスデータ読み込み
            for i in range(len(input_eye)):#時間の書き換え
                t_stamp=input_eye.iloc[i,0]
                #print(t_stamp)
                start_dt=dt.datetime.strptime(t_stamp,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
                start_unix=start_dt.timestamp() #UNIX時間に
                input_eye.iloc[i,0]=start_unix
            input_eye.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv',  index=False)#ファイルに出力

            input_eyev=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_valid.csv', index_col=None)#マウスデータ読み込み
            for i in range(len(input_eyev)):#時間の書き換え
                t_stamp=input_eyev.iloc[i,0]
                start_dt=dt.datetime.strptime(t_stamp,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
                start_unix=start_dt.timestamp() #UNIX時間に
                input_eyev.iloc[i,0]=start_unix

            input_eyev.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_valid.csv',  index=False)#ファイルに出力
            print(sm+dy+fn)