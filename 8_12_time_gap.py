import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.spatial import distance
import datetime as dt


timegap=[]
pre=[]
post=[]
input_eye=pd.read_csv('timegap.csv', header=None,index_col=None)#視線データ
for i in range(0,5):
    for j in range(0,len(input_eye.loc[i*3,:])):
        timegap.append(input_eye.loc[i*3,j])
        pre.append(input_eye.loc[(i+1)*3-2,j])
        post.append(input_eye.loc[(i+1)*3-1,j])
# print(len(timegap),timegap)
# print(len(pre))
# print(len(post))
print("------------pre-----------")
plt.scatter(timegap,pre)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in timegap]
clf.fit(X2, pre) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("平均時間差", fontname="MS Gothic")
plt.ylabel("事前自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
print("切片= ", '{:.3f}'.format (clf.intercept_))
print("決定係数= ", '{:.3f}'.format (clf.score(X2, pre)))
s1=pd.Series(timegap)
s2=pd.Series(pre)
print("相関係数= ",'{:.3f}'.format (s1.corr(s2)))

print("-------post------")
plt.scatter(timegap,post)
#plt.xlim(0,100)
plt.ylim(0,100)
clf = linear_model.LinearRegression()
X2 = [[x] for x in timegap]
clf.fit(X2, post) # 予測モデルを作成
plt.plot(X2, clf.predict(X2))
plt.xlabel("平均時間差", fontname="MS Gothic")
plt.ylabel("事後自己効力感", fontname="MS Gothic")
plt.show()
print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
print("切片= ", '{:.3f}'.format (clf.intercept_))
print("決定係数= ", '{:.3f}'.format (clf.score(X2, post)))
s1=pd.Series(timegap)
s2=pd.Series(post)
print("相関係数= ",'{:.3f}'.format (s1.corr(s2)))