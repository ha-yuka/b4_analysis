import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.spatial import distance
import datetime as dt

#サッカード回数

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','nomura','ota','shigenawa','suzuki','tabata','tamaru','tamura','watanabe','yashiro']#,,,'motoyama'
file_name = ['puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
#'n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']'n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5',
day = ['02']
pre=[]
post=[]
output_df=pd.DataFrame(columns=someone,index=file_name)
saccade_kyori=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            saccade=0
            #=================アンケートの結果=================
            if dy=='01':
                index=(task01.index[task01['被験者']==sm])[0]
                pre_q=fn+'_first'
                post_q=fn+'_last'
                pre.append(task01.loc[index,pre_q])
                post.append(task01.loc[index,post_q])
            else:
                index=(task02.index[task02['被験者']==sm])[0]
                pre_q=fn+'_first'
                post_q=fn+'_last'
                pre.append(task02.loc[index,pre_q])
                post.append(task02.loc[index,post_q])
            #print(index)
            #===============================================
            obj_df=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'obj.csv', index_col=None)#視線データ
            objnum=0
            flag=0
            for i in range(len(obj_df)):
                #print(i,objnum,obj_df.loc[i,'Obj num'])
                if objnum-obj_df.loc[i,'Obj num']==4:
                    #print("b")
                    pre_end=obj_df.loc[i-1,'Recording timestamp']
                    break 
                objnum=obj_df.loc[i,'Obj num']
            print(sm,fn,pre_end,i)
            input_df=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視線データ
            for i in range(len(input_df)):
                if input_df.loc[i,'Recording timestamp']>pre_end:
                    pre_end_ind=i-1
                    break 
  
            input_df= input_df.drop(range(0,i))
            input_df = input_df.reset_index(drop=True)#インデックス振り直し

            P_START = [[]]  # サッカードの開始点を全て格納（相対サッカード角度の計算で使う）
            P_END=[[]]
            p_start = []  # サッカードの開始点を格納（サッカード振幅）
            p_end = []  # サッカードの終了点を格納（サッカード振幅）
            amp_list = []  # サッカード振幅を格納
            drt_list_s = []  # ウィンドウ内のサッカード時間を格納

            sac_index = input_df.index[((input_df['Eye movement type'] == 'Saccade') | (input_df['Eye movement type'] == 'Unclassified'))].tolist()# ウィンドウ内の
            if sac_index[0]==0:
                x = input_df.at[input_df.index[0], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[0], 'Gaze point Y']  # 視点のy座標
                p_start =  [x, y]
                P_START.append(0)
                if sac_index[0]+1!=sac_index[1]:
                    x = input_df.at[input_df.index[sac_index[0] + 1], 'Gaze point X']  # 視点のx座標
                    y = input_df.at[input_df.index[sac_index[0] + 1], 'Gaze point Y']  # 視点のy座標
                    p_end = [x, y]
                    P_END.append(sac_index[0]) 
            else:
                x = input_df.at[input_df.index[sac_index[0] - 1], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[sac_index[0] - 1], 'Gaze point Y']  # 視点のy座標
                p_start =  [x, y]
                P_START.append(sac_index[0])
                if sac_index[0]+1!=sac_index[1]:
                    x = input_df.at[input_df.index[sac_index[0] + 1], 'Gaze point X']  # 視点のx座標
                    y = input_df.at[input_df.index[sac_index[0] + 1], 'Gaze point Y']  # 視点のy座標
                    p_end = [x, y]
                    P_END.append(sac_index[0])

            for k in range(1, len(sac_index) - 1):
                if sac_index[k - 1] + 1 != sac_index[k]:
                    x = input_df.at[input_df.index[sac_index[k] - 1], 'Gaze point X']  # 視点のx座標
                    y = input_df.at[input_df.index[sac_index[k] - 1], 'Gaze point Y']  # 視点のy座標
                    p_start =  [x, y]
                    P_START.append(sac_index[k])
                    
                if sac_index[k] + 1 != sac_index[k + 1]:
                    if P_START:#saccadeがあるとき
                        x = input_df.at[input_df.index[sac_index[k] + 1], 'Gaze point X']  # 視点のx座標
                        y = input_df.at[input_df.index[sac_index[k] + 1], 'Gaze point Y']  # 視点のy座標
                        p_end = [x, y]
                        P_END.append(sac_index[k])
                        amp_list.append(distance.euclidean(p_start, p_end))  # サッカード振幅を計算
            

            if (sac_index[-2] + 1 != sac_index[-1]) and (sac_index[-1] < len(input_df)-1):#ケツが連続でないかつ末尾でない
                x = input_df.at[input_df.index[sac_index[-1] - 1], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[sac_index[-1] - 1], 'Gaze point Y']  # 視点のy座標
                p_start = [x, y]
                P_START.append(sac_index[-1])
                x = input_df.at[input_df.index[sac_index[-1] + 1], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[sac_index[-1] + 1], 'Gaze point Y']  # 視点のy座標
                p_end = [x, y]
                P_END.append(sac_index[-1])
                if not (np.isnan(p_start).any() or np.isnan(p_end).any()):
                    amp_list.append(distance.euclidean(p_start, p_end))  # サッカード振幅を計算
            elif (sac_index[-2] + 1 != sac_index[-1]) and (sac_index[-1] == len(input_df)-1):#ケツが連続でないかつ末尾
                x = input_df.at[input_df.index[sac_index[-1] - 1], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[sac_index[-1] - 1], 'Gaze point Y']  # 視点のy座標
                p_start = [x, y]
                P_START.append(sac_index[-1])
                x = input_df.at[input_df.index[len(input_df)-1], 'Gaze point X']  # 視点のx座標
                y = input_df.at[input_df.index[len(input_df)-1], 'Gaze point Y']  # 視点のy座標
                p_end = [x, y]
                P_END.append(sac_index[-1])
                if not (np.isnan(p_start).any() or np.isnan(p_end).any()):
                    amp_list.append(distance.euclidean(p_start, p_end))  # サッカード振幅を計算
            elif (sac_index[-2] + 1 == sac_index[-1]):#ケツが連続
                if (sac_index[-1] == len(input_df)-1):#末尾
                    x = input_df.at[input_df.index[len(input_df)-1], 'Gaze point X']  # 視点のx座標
                    y = input_df.at[input_df.index[len(input_df)-1], 'Gaze point Y']  # 視点のy座標
                    p_end = [x, y]
                    P_END.append(sac_index[-1])
                else:#末尾でない
                    x = input_df.at[input_df.index[sac_index[-1]+1], 'Gaze point X']  # 視点のx座標
                    y = input_df.at[input_df.index[sac_index[-1]+1], 'Gaze point Y']  # 視点のy座標
                    p_end = [x, y]
                    P_END.append(sac_index[-1])
                if not (np.isnan(p_start).any() or np.isnan(p_end).any()):
                    amp_list.append(distance.euclidean(p_start, p_end))  # サッカード振幅を計算
            
            print("#===========================#")
            print('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv')
                
            saccade_kyori.append(sum(amp_list)/len(amp_list))  # 平均サッカード距離
            output_df.loc[fn,sm]=sum(amp_list)/len(amp_list)

output_df.to_excel("./sac_kyori_first.xlsx")
