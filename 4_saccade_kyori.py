import numpy as np
import pandas as pd
from scipy.spatial import distance
import datetime as dt

P_START = [[]]  # サッカードの開始点を全て格納（相対サッカード角度の計算で使う）
P_END = [[]]  # サッカードの終了点を全て格納（相対サッカード角度の計算で使う）
p_start = []  # サッカードの開始点を格納（サッカード振幅）
p_end = []  # サッカードの終了点を格納（サッカード振幅）
SAC_START = []  # サッカードの開始時刻を全て格納
SAC_END = []  # サッカードの終了時刻を全て格納
amp_list = []  # サッカード振幅を格納
drt_list_s = []  # ウィンドウ内のサッカード時間を格納

input_df=pd.read_csv('exp_data/'+'imahashi'+'01'+'/remove/' + 'iraira1-1'+'_'+ 'eye_all.csv', index_col=None)
# ウィンドウ内のsaccadeに該当するindexを格納
sac_index = input_df.index[((input_df['Eye movement type'] == 'Saccade') | (
         input_df['Eye movement type'] == 'Unclassified'))].tolist()

for k in range(1, len(sac_index) - 1):
    if sac_index[k - 1] + 1 != sac_index[k]:
        x = input_df.at[input_df.index[sac_index[k] - 1], 'Gaze point X']  # 視点のx座標
        y = input_df.at[input_df.index[sac_index[k] - 1], 'Gaze point Y']  # 視点のy座標
        p_start = [x, y]
        P_START.append(p_start)
        sac_start = input_df.at[input_df.index[sac_index[k] - 1], 'Recording timestamp']  # サッカード開始時刻
        start_dt=dt.datetime.strptime(sac_start,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
        start_unix=start_dt.timestamp() #UNIX時間に
        SAC_START.append(start_unix)

    if sac_index[k] + 1 != sac_index[k + 1]:
        if P_START:
            x = input_df.at[input_df.index[sac_index[k] + 1], 'Gaze point X']  # 視点のx座標
            y = input_df.at[input_df.index[sac_index[k] + 1], 'Gaze point Y']  # 視点のy座標
            p_end = [x, y]
            P_END.append(p_end)
            sac_end = input_df.at[input_df.index[sac_index[k] + 1], 'Recording timestamp']  # サッカード終了時刻
            end_dt=dt.datetime.strptime(sac_end,'%Y-%m-%d %H:%M:%S.%f') #datetime型に
            end_unix=end_dt.timestamp() #UNIX時間に
            SAC_END.append(end_unix)
            # print('=======================')
            # print('p_start: ', p_start)
            # print('p_end', p_end)
            # print('sac_start: ', sac_start)
            # print('sac_end: ', sac_end)
            #print('win_start: ',input_df.at[input_df.index[win_index[0]], 'Recording timestamp'])
            if not (np.isnan(p_start).any() or np.isnan(p_end).any()):
                amp_list.append(distance.euclidean(p_start, p_end))  # サッカード振幅を計算
            else:
                amp_list.append(np.nan)
            
            jikan=(end_unix - start_unix)
            drt_list_s.append(jikan / 1000)  # サッカード時間を計算

sp_list = [m / n for (m, n) in zip(amp_list, drt_list_s)]  # サッカード速度
