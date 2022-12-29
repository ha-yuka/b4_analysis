import pandas as pd
import datetime as dt
from decimal import *

################csvファイルから必要な時間の抽出#################
input_obj=pd.read_csv('exp_data/' + 'imahashi'+ '01/' +'imahashi01_obj/'+ 'iraira1-1.csv',header=None)#ファイルの読み込み

start=input_obj.iloc[0,0] #○○○○‐○○‐○○ ○○:○○:○○,○○○○
start_dt=dt.datetime.strptime(start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
start_unix=start_dt.timestamp() #UNIX時間に

end=input_obj.iloc[-1,0]
end_dt=dt.datetime.strptime(end,'%Y-%m-%d %H:%M:%S.%f')
end_unix=end_dt.timestamp() #UNIX時間に
print(end_dt-start_dt)
#print("start=",start_unix)
#print("end  =",end_unix)
######################################################################

###############################アイトラッカーアイトラッカーデータ#############################
input_data=pd.read_excel('exp_data/' + 'imahashi'+ '01/' +'Data Export - '+'imahashi01/'+ 'imahashi'+'01 '+'iraira1-1.xlsx',index_col=None)#ファイルの読み込み
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

for i in range(start_index,len(input_data)):#終了点探索
    pass_time=input_data.loc[i,'Recording timestamp']
    time=round(pass_time*0.000001,6)#秒に変換
    now_unix=recording_st_unix+time
    if now_unix>end_unix:
        end_index=i
        break


input_data=input_data.drop(range(end_index,len(input_data)))#最後の余分な部分削除
input_data= input_data.drop([i for i in range(start_index-1)])#最初の余分な部分削除
input_data = input_data.loc[:,['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Mouse position X','Mouse position Y']]
input_data = input_data.reset_index(drop=True)#インデックス振り直し

for i in range(len(input_data)):#時間の書き換え
    t_stamp=input_data.iloc[i,0]
    new_unix=round(t_stamp*0.000001,6)+recording_st_unix
    new_dt = dt.datetime.fromtimestamp(new_unix)
    input_data.iloc[i,0]=new_dt


eyetracker_df=input_data#コピー
drop_index=eyetracker_df.index[eyetracker_df['Sensor']!='Eye Tracker']
eyetracker_df=eyetracker_df.drop(drop_index)
eyetracker_df = eyetracker_df.reset_index(drop=True)
eyetracker_df = eyetracker_df.loc[:,['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right']]
eyetracker_df.to_csv('exp_data/imahashi01/remove/' + 'imahashi01_'+ 'eye_all.csv',  index=False)#視線データ（invalidあり）ファイルに出力

drop_index=eyetracker_df.index[(eyetracker_df['Validity left']=='Invalid') & (eyetracker_df['Validity right']=='Invalid')]
eyetracker_df=eyetracker_df.drop(drop_index)
eyetracker_df = eyetracker_df.reset_index(drop=True)
eyetracker_df.to_csv('exp_data/imahashi01/remove/' + 'imahashi01_'+ 'eye_valid.csv',  index=False)#ファイルに出力（invalidなし）

################マウスデータ出力#######################
drop_index=input_data.index[input_data['Sensor']!='Mouse']
input_data=input_data.drop(drop_index)
input_data = input_data.reset_index(drop=True)
input_data = input_data.loc[:,['Recording timestamp','Event','Sensor','Mouse position X','Mouse position Y']]
input_data.to_csv('exp_data/imahashi01/remove/' + 'imahashi01_'+ 'mouse.csv',  index=False)#ファイルに出力


#mouse_df.to_csv('data/kawamura01/remove/' + 'kawamura_iraira1mouse_test'+ ' Data Export Trim.csv',  index=False)#ファイルに出力
######################################################################

"""
print(round(input_mouse.iloc[start_index-1,0]*0.000001,6)+mouse_st_unix)
print(round(input_mouse.iloc[start_index,0]*0.000001,6)+mouse_st_unix)
print(round(input_mouse.iloc[start_index+1,0]*0.000001,6)+mouse_st_unix)
print("=====================")
print(round(input_mouse.iloc[end_index-1,0]*0.000001,6)+mouse_st_unix)
print(round(input_mouse.iloc[end_index,0]*0.000001,6)+mouse_st_unix)
print(round(input_mouse.iloc[end_index+1,0]*0.000001,6)+mouse_st_unix)
"""
