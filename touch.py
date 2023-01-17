import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

#接触時間とアンケート

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro']#'tamura',,'watanabe',,
file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
#file_name=['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
day = ['01', '02']

touch=[]
puzzle_pre=[]
puzzle_post=[]
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
                pre=fn+'_pre'
                post=fn+'_post'
                puzzle_pre.append(task01.loc[index,pre])
                puzzle_post.append(task01.loc[index,post])
            else:
                index=(task02.index[task02['被験者']==sm])[0]
                pre=fn+'_pre'
                post=fn+'_post'
                puzzle_pre.append(task02.loc[index,pre])
                puzzle_post.append(task02.loc[index,post])
            #================================================
            total=0 #視線データの数
            eye_index=0

            input_touch=pd.read_csv('exp_data/'+sm+dy+'/'+sm+dy+'_obj/touch.csv', index_col=None,header=None)#視線データ読み込み
            index=(input_touch.index[input_touch[1]==fn])[0]
            #print(index)

            num=input_touch.loc[index,2]

            touch.append(num)


print("-------------------pre--------------------")
plt.scatter(touch,puzzle_pre)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in touch]
clf.fit(X2, puzzle_pre) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
#ax.text(19.0, 0.6, '$ R^{2} $=' + str(round(r2_lin, 4)))
#plt.plot(df_x, y_lin_fit, color = '#000000', linewidth=0.5)
plt.xlabel("接触回数", fontname="MS Gothic")
plt.ylabel("事前自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数= ", clf.coef_)
print("切片= ", clf.intercept_)
print("決定係数= ", clf.score(X2, puzzle_pre))
s1=pd.Series(touch)
s2=pd.Series(puzzle_pre)
print(s1.corr(s2))

print("----------------post----------------")
plt.scatter(touch,puzzle_post)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in touch]
clf.fit(X2, puzzle_post) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("接触回数", fontname="MS Gothic")
plt.ylabel("事後自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数= ", clf.coef_)
print("切片= ", clf.intercept_)
print("決定係数= ", clf.score(X2, puzzle_post))
s1=pd.Series(touch)
s2=pd.Series(puzzle_post)
print(s1.corr(s2))