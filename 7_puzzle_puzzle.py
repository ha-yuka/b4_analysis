import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.spatial import distance
import datetime as dt

def outlier_2s(li):
    # 平均と標準偏差
    out_index=[]
    average = np.mean(li)
    sd = np.std(li)
    # 外れ値の基準点
    outlier_min = average - (sd) * 3
    outlier_max = average + (sd) * 3
    for i in range(0,len(li)):
        if li[i]<outlier_min:
            out_index.append(i)
        # 範囲から外れている値を除く
        elif li[i]>outlier_max:
            out_index.append(i)
    for i in range(0, len(out_index)):
        li.pop(out_index[len(out_index)-1-i])

    return li

someone = ['yashiro']#'tamura',,,,,'kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro','watanabe''imahashi'
#file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
file_name=['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
day = ['01', '02']
pre=[]
post=[]
col_name=['Recording timestamp','pre_area','post_area']

time_gap=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            sub_gap=[]
            mouse_t=[]
            eye_t=[]

            #=================アンケートの結果=================#
            if dy=='01':
                index=(task01.index[task01['被験者']==sm])[0]
                pre_q=fn+'_pre'
                post_q=fn+'_post'
                pre.append(task01.loc[index,pre_q])
                post.append(task01.loc[index,post_q])
            else:
                index=(task02.index[task02['被験者']==sm])[0]
                pre_q=fn+'_pre'
                post_q=fn+'_post'
                pre.append(task02.loc[index,pre_q])
                post.append(task02.loc[index,post_q])
            #===============================================#
            #========================オブジェクトの移動======================#
            input_obj=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'obj.csv', index_col=None)#オブジェクト操作データ
            #input_obj.columns=['Recording timestamp','Obj_num','Position X','Position Y']
            for i in range(0,len(input_obj)-1):#オブジェクトの位置1行ずつ見ていく
                obj=input_obj.loc[i,'Obj num']
                if input_obj.loc[i,'Position X']>1050:
                    t_obj=2 #右にある
                elif 850<=input_obj.loc[i,'Position X']<=1050:
                    t_obj=1 #中央にある
                elif input_obj.loc[i,'Position X']<850:
                    t_obj=0 #左にある

                obj_1=input_obj.loc[i+1,'Obj num']
                if input_obj.loc[i+1,'Position X']>1050:
                    t_1_obj=2 #右にある
                elif 850<=input_obj.loc[i+1,'Position X']<=1050:
                    t_1_obj=1 #中央にある
                elif input_obj.loc[i+1,'Position X']<850:
                    t_1_obj=0 #左にある

                if abs(t_obj-t_1_obj)==1 and obj==obj_1:
                    mouse_t.append([input_obj.loc[i,'Recording timestamp'],t_obj,t_1_obj])
                    #print(obj, obj_1,t_obj,t_1_obj)
            mouse_df=pd.DataFrame(mouse_t,columns=col_name)
            #print(mouse_in)
            #=======================視線の移動============================#
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視線データ
            #['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type']
            for i in range(0,len(input_eye)-1):#オブジェクトの位置1行ずつ見ていく
                #if input_eye.loc[i,'Gaze point X']==
                if input_eye.loc[i,'Gaze point X']>1050:
                    t_eye=2 #右にある
                elif 850<=input_eye.loc[i,'Gaze point X']<=1050:
                    t_eye=1 #中央にある
                elif input_eye.loc[i,'Gaze point X']<850:
                    t_eye=0 #左にある

                if input_eye.loc[i+1,'Gaze point X']>1050:
                    t_1_eye=2 #右にある
                elif 850<=input_eye.loc[i+1,'Gaze point X']<=1050:
                    t_1_eye=1 #中央にある
                elif input_eye.loc[i+1,'Gaze point X']<850:
                    t_1_eye=0 #左にある

                if abs(t_eye-t_1_eye)==1:
                    eye_t.append([input_eye.loc[i,'Recording timestamp'],t_eye,t_1_eye])
            eye_df=pd.DataFrame(eye_t,columns=col_name)
            #print(eye_in)

            #==================時間差算出==================#
            two_one_index = eye_df.index[((eye_df['pre_area'] == 2) & (eye_df['post_area'] == 1))].tolist()#2→1
            two_one_df=eye_df.loc[two_one_index,]
            one_zero_index = eye_df.index[((eye_df['pre_area'] == 1) & (eye_df['post_area'] ==0))].tolist()#1→0
            one_zero_df=eye_df.loc[one_zero_index,]
            zero_one_index = eye_df.index[((eye_df['pre_area'] == 0) & (eye_df['post_area'] == 1))].tolist()#0→1
            zero_one_df=eye_df.loc[zero_one_index,]
            one_two_index = eye_df.index[((eye_df['pre_area'] == 1) & (eye_df['post_area'] == 2))].tolist()#1→2
            one_two_df=eye_df.loc[one_two_index,]
            # print("==========================")
            # print(two_one_df)
            # print(one_zero_df)
            # print(zero_one_df)
            # print(one_two_df)
            for i in range(0,len(mouse_df)):
                pre_a=mouse_df.loc[i,'pre_area']
                post_a=mouse_df.loc[i,'post_area']
                t=mouse_df.loc[i,'Recording timestamp']
                if (pre_a==2 and post_a==1) or (pre_a==0 and post_a==1):#2→1,0→1
                    inear_1=two_one_df['Recording timestamp'].sub(t).abs().idxmin()
                    inear_2=zero_one_df['Recording timestamp'].sub(t).abs().idxmin()
                    near_1=two_one_df.loc[inear_1,'Recording timestamp']
                    near_2=zero_one_df.loc[inear_2,'Recording timestamp']
                    if abs(t-near_1)<(t-near_2):
                        u=near_1
                    else:
                        u=near_2
                elif pre_a==1 and post_a==0:#1→0
                    near=one_zero_df['Recording timestamp'].sub(t).abs().idxmin()
                    u=one_zero_df.loc[near,'Recording timestamp']
                else:#1→2
                    near=one_two_df['Recording timestamp'].sub(t).abs().idxmin()
                    u=one_two_df.loc[near,'Recording timestamp']
                sub_gap.append(t-u)          
            sub_gap_out=outlier_2s(sub_gap) 
            print(sub_gap,sum(sub_gap_out)/len(sub_gap_out))
            #print(sm,dy,fn)            
            time_gap.append(sum(sub_gap_out)/len(sub_gap_out))  # 平均サッカード距離

print("-------------------pre--------------------")
plt.scatter(time_gap,pre)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in time_gap]
clf.fit(X2, pre) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("平均時間差", fontname="MS Gothic")
plt.ylabel("事前自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数= ", clf.coef_)
print("切片= ", clf.intercept_)
print("決定係数= ", clf.score(X2, pre))
s1=pd.Series(time_gap)
s2=pd.Series(pre)
print(s1.corr(s2))

print("----------------post----------------")
plt.scatter(time_gap,post)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in time_gap]
clf.fit(X2, post) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("平均時間差", fontname="MS Gothic")
plt.ylabel("事後自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数= ", clf.coef_)
print("切片= ", clf.intercept_)
print("決定係数= ", clf.score(X2, post))
s1=pd.Series(time_gap)
s2=pd.Series(post)
print(s1.corr(s2))