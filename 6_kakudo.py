import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import datetime as dt

#クリック直後の視線とマウスの動く角度

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro']#'tamura',,'watanabe',,
file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
#file_name=['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
day = ['01', '02']
pre=[]
post=[]

kakudo=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
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
            #print(index)
            #================================================
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv', index_col=None)#マウスデータ読み込み
            click_index = input_eye.index[(input_eye['Event value'] == 'Down, Left')].tolist()#クリックのインデックス取得|(input_eye['Event value'] == 'Up, Left')
            min=100
            for i in range(0,len(click_index)-1):
                gap=click_index[i+1]-click_index[i]
                if min>gap:
                    min=gap
            print(sm,dy,fn,min)

            

# print("-------------------pre--------------------")
# plt.scatter(pass_time,pre)
# #plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in pass_time]
# clf.fit(X2, pre) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# #ax.text(19.0, 0.6, '$ R^{2} $=' + str(round(r2_lin, 4)))
# #plt.plot(df_x, y_lin_fit, color = '#000000', linewidth=0.5)
# plt.xlabel("実行時間", fontname="MS Gothic")
# plt.ylabel("事前自己効力感", fontname="MS Gothic")
# plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, pre))
# s1=pd.Series(pass_time)
# s2=pd.Series(pre)
# print(s1.corr(s2))

# print("----------------post----------------")
# plt.scatter(pass_time,post)
# #plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in pass_time]
# clf.fit(X2, post) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# plt.xlabel("実行時間", fontname="MS Gothic")
# plt.ylabel("事後自己効力感", fontname="MS Gothic")
# plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, post))
# s1=pd.Series(pass_time)
# s2=pd.Series(post)
# print(s1.corr(s2))