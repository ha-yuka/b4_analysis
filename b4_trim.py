import pandas as pd
import datetime as dt
from decimal import *

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','motoyama','nomura','ota','shigenawa','suzuki','tabata','tamaru','watanabe','yashiro']#'tamura'
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']#,
day = ['01', '02']
df=pd.DataFrame(columns=file_name)
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
            #print(end_dt-start_dt)
            """
            ################csvファイルから必要な時間の抽出#################
            input_obj=pd.read_csv('exp_data/' + sm+ dy +'/'+sm+dy+'_obj/'+ fn+'.csv',header=None)#ファイルの読み込み

            start=input_obj.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
            start_dt=dt.datetime.strptime(start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
            start_unix=start_dt.timestamp() #UNIX時間に

            end=input_obj.iloc[-1,0]
            end_dt=dt.datetime.strptime(end,'%Y-%m-%d %H:%M:%S.%f')
            end_unix=end_dt.timestamp() #UNIX時間に
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


            input_data=input_data.drop(range(end_index,len(input_data)))#最後の余分な部分削除
            input_data= input_data.drop([i for i in range(start_index)])#最初の余分な部分削除
            input_data = input_data.loc[:,['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type','Mouse position X','Mouse position Y','Event value']]
            input_data = input_data.reset_index(drop=True)#インデックス振り直し

            for i in range(len(input_data)):#時間の書き換え
                t_stamp=input_data.iloc[i,0]
                new_unix=round(t_stamp*0.000001,6)+recording_st_unix
                new_dt = dt.datetime.fromtimestamp(new_unix)
                input_data.iloc[i,0]=new_dt
            
            pass_time=input_data.iloc[-1,0]-input_data.iloc[0,0]
            l_sm.append(pass_time)
            print(pass_time)

            eyetracker_df=input_data#コピー
            drop_index=eyetracker_df.index[eyetracker_df['Sensor']!='Eye Tracker']
            eyetracker_df=eyetracker_df.drop(drop_index)
            eyetracker_df = eyetracker_df.reset_index(drop=True)
            eyetracker_df = eyetracker_df.loc[:,['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type']]
            eyetracker_df.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv',  index=False)#視線データ（invalidあり）ファイルに出力

            drop_index=eyetracker_df.index[((eyetracker_df['Validity left']=='Invalid') & (eyetracker_df['Validity right']=='Invalid'))]
            eyetracker_df=eyetracker_df.drop(drop_index)
            eyetracker_df = eyetracker_df.reset_index(drop=True)
            eyetracker_df.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_valid.csv',  index=False)#ファイルに出力（invalidなし）

            ################マウスデータ出力#######################
            drop_index=input_data.index[((input_data['Event']!='MouseEvent')&(input_data['Sensor']!='Mouse'))]
            input_data=input_data.drop(drop_index)
            input_data = input_data.reset_index(drop=True)
            input_data = input_data.loc[:,['Recording timestamp','Sensor','Mouse position X','Mouse position Y','Event','Event value']]
            input_data.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv',  index=False)#ファイルに出力
            print(sm+dy)
            """


        df.loc[sm+dy]=l_sm#被験者smのdy日目の時間をデータフレームに追加
        
df.to_csv('test.csv')#時間の情報をcsvに