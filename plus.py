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
#print("start=",start_unix)
#print("end  =",end_unix)
######################################################################

###############################マウスデータ#############################
input_mouse=pd.read_excel('exp_data/' + 'imahashi'+ '01/' + 'Data Export - '+'imahashi01/'+ 'imahashi'+'01 '+'iraira1-1.xlsx',index_col=None)#ファイルの読み込み
mouse_st=input_mouse.loc[0,'Recording date']+' '+input_mouse.loc[0,'Recording start time']
mouse_st_dt=dt.datetime.strptime(mouse_st,'%Y/%m/%d %H:%M:%S.%f')
mouse_st_unix=mouse_st_dt.timestamp()

for i in range(len(input_mouse)): #開始点探索
    pass_time=input_mouse.loc[i,'Recording timestamp']
    time=round(pass_time*0.000001,6)#秒に変換
    #print(time)
    now_unix=mouse_st_unix+time
    if now_unix>start_unix:
        start_index=i
        break

for i in range(len(input_mouse)):#終了点探索
    pass_time=input_mouse.loc[i,'Recording timestamp']
    time=round(pass_time*0.000001,6)#秒に変換
    now_unix=mouse_st_unix+time
    if now_unix>end_unix:
        end_index=i
        break

input_mouse=input_mouse.drop(range(end_index+1,len(input_mouse)))
input_mouse= input_mouse.drop([i for i in range(start_index-1)])
mouse_df = input_mouse.loc[:,['Recording timestamp','Event','Mouse position X','Mouse position Y','Gaze point X','Gaze point Y','Validity left','Validity right']]
mouse_df = mouse_df.reset_index(drop=True)
for i in range(len(mouse_df)):
    t_stamp=mouse_df.iloc[i,0]
    new_mouse_unix=round(t_stamp*0.000001,6)+mouse_st_unix
    new_mouse_dt = dt.datetime.fromtimestamp(new_mouse_unix)
    mouse_df.iloc[i,0]=new_mouse_dt

mouse_df.to_csv('exp_data/imahashi01/remove/' + 'imahashi_iraira1'+ ' Data Export Trim.csv',  index=False)#ファイルに出力
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
