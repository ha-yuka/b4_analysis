import pandas as pd
import datetime as dt
from decimal import *

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','motoyama','nomura','ota','shigenawa','suzuki','tabata','tamaru','watanabe','yashiro','tamura']#,,
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2','puzzle5-1','puzzle5-2']
day = ['02']#'01'
for sm in someone:
    for dy in day:
        l_sm=[]
        for fn in file_name:            
            print(sm,dy,fn)
            ################csvファイルから必要な時間の抽出#################
            input_obj=pd.read_csv('exp_data/' + sm+ dy +'/remove/'+fn+'_obj.csv',index_col=None)#ファイルの読み込み
            start_unix=input_obj.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
            #print(start_unix)
            
            end_unix=input_obj.iloc[-1,0]
            ##############################################################
            
            ###############################アイトラッカーアイトラッカーデータ#############################
            input_data=pd.read_excel('exp_data/' + sm+ dy +'/Data Export - '+sm+dy+ '/'+sm+dy+' '+fn+'.xlsx',index_col=None)#ファイルの読み込み
            recording_st=input_data.loc[0,'Recording date']+' '+input_data.loc[0,'Recording start time']
            recording_st_dt=dt.datetime.strptime(recording_st,'%Y/%m/%d %H:%M:%S.%f')
            recording_st_unix=recording_st_dt.timestamp()#レコーディング開始時刻

            for i in range(len(input_data)): #開始点探索
                pass_time=input_data.loc[i,'Recording timestamp']
                time=round(pass_time*0.000001,6)#秒に変換
                #print(time)
                now_unix=recording_st_unix+time
                #print(now_unix)
                if now_unix>start_unix:
                    start_index=i
                    break
            
            for i in range(start_index):
                check=input_data.loc[start_index-i,'Event']
                if check=='MouseEvent':
                    start_index=start_index-i
                    break


            for i in range(start_index,len(input_data)):#終了点探索
                pass_time=input_data.loc[i,'Recording timestamp']
                time=round(pass_time*0.000001,6)#秒に変換
                now_unix=recording_st_unix+time
                if now_unix>end_unix:
                    end_index=i
                    break

            
            input_data['Gaze point X'] = input_data['Gaze point X'].interpolate().tolist() #補間
            input_data['Gaze point Y'] = input_data['Gaze point Y'].interpolate().tolist() #補間

            input_data=input_data.drop(range(end_index,len(input_data)))#最後の余分な部分削除
            input_data= input_data.drop(range(0,start_index))#最初の余分な部分削除
            input_data = input_data.loc[:,['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type','Mouse position X','Mouse position Y','Event','Event value']]
            input_data = input_data.reset_index(drop=True)#インデックス振り直し

            for i in range(len(input_data)):#時間の書き換え
                t_stamp=input_data.loc[i,'Recording timestamp']
                new_unix=round(t_stamp*0.000001,6)+recording_st_unix
                input_data.loc[i,'Recording timestamp']=new_unix
            
            #print(pass_time)
            input_data.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv',  index=False)#ファイルに出力


            # ################マウスデータ出力#######################
            # drop_index=input_data.index[((input_data['Event']!='MouseEvent')&(input_data['Sensor']!='Mouse'))]
            # input_data=input_data.drop(drop_index)
            # input_data = input_data.reset_index(drop=True)
            # input_data = input_data.loc[:,['Recording timestamp','Sensor','Mouse position X','Mouse position Y','Event','Event value']]
            # input_data.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv',  index=False)#ファイルに出力
            # print(sm+dy+fn)
            