import pandas as pd
import datetime as dt
from decimal import *

someone = ['watanabe/','suzuki/']#,'shigenawa/','maeda/','kobayasi/','kawasaki/','tamura/','tamaru/','nomura/','motoyama/','ota/','kawamura/','imahashi/','yashiro/','tabata/']
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2',]
day = ['01', '02']
gfi = ''

for sm in someone:
    for fn in file_name:
        for dy in day:
            ################csvファイルから必要な時間の抽出#################
            input_obj=pd.read_csv('data/' + 'kawamura'+ '01/' +'obj/'+ 'iraira1-1.csv',header=None)#ファイルの読み込み

            start=input_obj.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
            start_dt=dt.datetime.strptime(start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
            start_unix=start_dt.timestamp() #UNIX時間に

            end=input_obj.iloc[-1,0]
            end_dt=dt.datetime.strptime(end,'%Y-%m-%d %H:%M:%S.%f')
            end_unix=end_dt.timestamp() #UNIX時間に
            #print("start=",start_unix)
            #print("end  =",end_unix)
            ##############################################################

            input_mouse=pd.read_excel('data/' + 'kawamura'+ '01/' +'mousedata/'+'Data Export - '+'kawamura01/'+ 'kawamura'+'01 '+'iraira1-1.xlsx',index_col=None)#ファイルの読み込み
            mouse_st=input_mouse.loc[0,'Recording date']+' '+input_mouse.loc[0,'Recording start time']
            mouse_st_dt=dt.datetime.strptime(mouse_st,'%Y/%m/%d %H:%M:%S.%f')
            mouse_st_unix=mouse_st_dt.timestamp()
            #print(mouse_st_unix)
            #text_df = input_mouse.drop(range(text_st_index[0] + 2))
            #print(input_mouse)
            for i in range(len(input_mouse)):
                pass_time=input_mouse.loc[i,'Recording timestamp']
                time=round(pass_time*0.000001,6)#秒に変換
                #print(time)
                now_unix=mouse_st_unix+time
                if now_unix>start_unix:
                    start_index=i
                    break

            for i in range(len(input_mouse)):
                pass_time=input_mouse.loc[i,'Recording timestamp']
                time=round(pass_time*0.000001,6)#秒に変換
                now_unix=mouse_st_unix+time
                if now_unix>end_unix:
                    end_index=i
                    break

            input_mouse=input_mouse.drop(range(end_index+1,len(input_mouse)))
            input_mouse= input_mouse.drop([i for i in range(start_index-1)])
            mouse_df = input_mouse.loc[:,['Recording timestamp','Event','Mouse position X','Mouse position Y']]
            mouse_df = mouse_df.reset_index(drop=True)
            for i in range(len(mouse_df)):
                t_stamp=mouse_df.iloc[i,0]
                new_mouse_unix=round(t_stamp*0.000001,6)+mouse_st_unix
                new_mouse_dt = dt.datetime.fromtimestamp(new_mouse_unix)
                mouse_df.iloc[i,0]=new_mouse_dt

  
            mouse_df.to_csv('data/remove/' + 'kawamura_test'+ ' Data Export Trim.csv',  index=False)#ファイルに出力
# print(df)
