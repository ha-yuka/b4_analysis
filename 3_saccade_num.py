import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import datetime as dt

#サッカード回数

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','nomura','ota','shigenawa','suzuki','tabata','tamaru','tamura','watanabe','yashiro']#01,02'motoyama'
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
day=['02']
pre=[]
post=[]
output_df=pd.DataFrame(columns=someone,index=file_name)
saccade_pers=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            print(sm,dy,fn)
            saccade=0
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
            #===============================================
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視線データ
            #======================所要時間計算=========================
            start_unix=input_eye.iloc[0,0] 
            end_unix=input_eye.iloc[-1,0]
            pass_time=(end_unix-start_unix)
            #===========================サッカード回数計算==============================
            sac_index = input_eye.index[((input_eye['Eye movement type'] == 'Saccade') | (input_eye['Eye movement type'] == 'Unclassified'))].tolist()# ウィンドウ内の
            if sac_index[0]==0:
                #print("1")
                saccade=saccade+1

            for k in range(1, len(sac_index) - 1):
                #print("2")
                if sac_index[k - 1] + 1 != sac_index[k]:
                    #print("a")
                    saccade=saccade+1
                    
            if (sac_index[-2] + 1 != sac_index[-1]):
               #print("3")
               saccade=saccade+1
            #print(saccade)
            
            saccade_pers.append(saccade/pass_time)
            #print(saccade_pers)
            output_df.loc[fn,sm]=saccade/pass_time

output_df.to_excel("./sac_num.xlsx")


print("-------------------pre--------------------")
plt.scatter(saccade_pers,pre)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in saccade_pers]
clf.fit(X2, pre) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("単位時間当たりのサッカード回数", fontname="MS Gothic")
plt.ylabel("事前自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
print("切片= ", '{:.3f}'.format (clf.intercept_))
print("決定係数= ", '{:.3f}'.format (clf.score(X2, pre)))
s1=pd.Series(saccade_pers)
s2=pd.Series(pre)
print("相関係数= ",'{:.3f}'.format (s1.corr(s2)))

print("----------post----------------")
plt.scatter(saccade_pers,post)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in saccade_pers]
clf.fit(X2, post) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("単位時間当たりのサッカード回数", fontname="MS Gothic")
plt.ylabel("事後自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
print("切片= ", '{:.3f}'.format (clf.intercept_))
print("決定係数= ", '{:.3f}'.format (clf.score(X2, post)))
s1=pd.Series(saccade_pers)
s2=pd.Series(post)
print("相関係数= ",'{:.3f}'.format (s1.corr(s2)))