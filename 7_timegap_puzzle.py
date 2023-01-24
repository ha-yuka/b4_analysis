import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.spatial import distance
import datetime as dt

#サッカード回数

someone = ['imahashi']#'tamura',,'watanabe',,,'kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro'
#file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
file_name=['n_puzzle1']#, 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2'
day = ['01', '02']
pre=[]
post=[]

time_gap=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            sub_gap=[]
            center_in=[]
            left_in=[]
            right_in=[]
            #=================アンケートの結果=================
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
            #===============================================
            input_obj=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'obj.csv', index_col=None)#オブジェクト操作データ
            #input_obj.columns=['Recording timestamp','Obj_num','Position X','Position Y']
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv', index_col=None)#視線データ

            for i in range(0,len(input_obj)-1):#オブジェクトの位置1行ずつ見ていく
                if input_obj.loc[i,'Position X']>1050:
                    t_obj=2 #右にある
                elif 850<=input_obj.loc[i,'Position X']<=1050:
                    t_obj=1 #中央にある
                elif input_obj.loc[i,'Position X']<850:
                    t_obj=0 #左にある
                
                if input_obj.loc[i+1,'Position X']>1050:
                    t_1_obj=2 #右にある
                elif 850<=input_obj.loc[i+1,'Position X']<=1050:
                    t_1_obj=1 #中央にある
                elif input_obj.loc[i+1,'Position X']<850:
                    t_1_obj=0 #左にある

                if t_obj!=t_1_obj:
                    print(t_obj,t_1_obj,"a")

            
            
            #time_gap.append(sum(sub_gap)/len(sub_gap))  # 平均サッカード距離

# print("-------------------pre--------------------")
# plt.scatter(saccade_kyori,pre)
# #plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in saccade_kyori]
# clf.fit(X2, pre) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# plt.xlabel("平均事前注視時間", fontname="MS Gothic")
# plt.ylabel("事前自己効力感", fontname="MS Gothic")
# plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, pre))
# s1=pd.Series(saccade_kyori)
# s2=pd.Series(pre)
# print(s1.corr(s2))

# print("----------------post----------------")
# plt.scatter(saccade_kyori,post)
# #plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in saccade_kyori]
# clf.fit(X2, post) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# plt.xlabel("平均事前注視時間", fontname="MS Gothic")
# plt.ylabel("事後自己効力感", fontname="MS Gothic")
# plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, post))
# s1=pd.Series(saccade_kyori)
# s2=pd.Series(post)
# print(s1.corr(s2))