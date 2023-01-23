import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import datetime as dt

#クリック直後の視線とマウスの動く角度

someone = ['imahashi']#'tamura',,'watanabe',,,'kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro'
file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
#file_name=['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
day = ['02']#'01',
pre=[]
post=[]
after=15

kakudo=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            #========================接触回数の確認======================#
            input_touch=pd.read_csv('exp_data/'+sm+dy+'/'+sm+dy+'_obj/touch.csv', index_col=None,header=None)#接触回数データ読み込み
            index=(input_touch.index[input_touch[1]==fn])[0]
            #print(index)
            num=input_touch.loc[index,2]
            if num==0:
                break
                #kakudo.append(0)
            #=================アンケートの結果=================
            mouse_start=[]
            mouse_end=[]
            eye_start=[]
            eye_end=[]
            pop_index=[]
            k_list=[]
            start_time=0
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
            input_mouse=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv', index_col=None)#マウスデータ読み込み
            click_index = input_mouse.index[(input_mouse['Event value'] == 'Down, Left')].tolist()#クリックのインデックス取得
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視線データ読み込み
            if len(click_index)>=2:
                for i in range(1,len(click_index)):
                    if click_index[i]-click_index[i-1]<=after:
                        pop_index.append(i-1)
            for i in range(0, len(pop_index)):#近すぎるクリックインデックス消す
                click_index.pop(pop_index[len(pop_index)-1-i])

            if len(click_index)>=2:
                for i in range(0,len(click_index)-1):
                    a = input_mouse.at[input_mouse.index[i], 'Mouse position X']  # 視点のx座標
                    b = input_mouse.at[input_mouse.index[i], 'Mouse position Y']  # 視点のy座標
                    mouse_start=[a, b]
                    c = input_mouse.at[input_mouse.index[i+after], 'Mouse position X']  # 視点のx座標
                    d = input_mouse.at[input_mouse.index[i+after], 'Mouse position Y']  # 視点のy座標
                    mouse_end=[c, d]
                    mouse_vec=np.array([c-a,d-b])
                    sac_start = input_mouse.at[input_mouse.index[click_index[i]], 'Recording timestamp']  # サッカード開始時刻
                    ind=input_eye['Recording timestamp'].sub(sac_start).abs().idxmin()#最も近い時間の値
                    e = input_eye.at[input_eye.index[ind], 'Gaze point X']  # 視点のx座標
                    f = input_eye.at[input_eye.index[ind], 'Gaze point Y']  # 視点のy座標
                    eye_start=[e, f]
                    g = input_eye.at[input_eye.index[ind+after], 'Gaze point X']  # 視点のx座標
                    h = input_eye.at[input_eye.index[ind+after], 'Gaze point Y']  # 視点のy座標
                    eye_end=[g, h]
                    eye_vec=np.array([g-e,h-f])
                    naiseki=np.inner(eye_vec,mouse_vec)
                    theta=np.arccos(naiseki/(np.linalg.norm(eye_vec)*np.linalg.norm(mouse_vec)))
                    k_list.append(theta)
    
                    # print("=====================================")
                    # print(eye_start)
                    # print(eye_end)
                    #print(eye_vec)


            if click_index[-1]+after<len(input_mouse)-1:
                    a = input_mouse.at[input_mouse.index[click_index[-1]], 'Mouse position X']  # 視点のx座標
                    b = input_mouse.at[input_mouse.index[click_index[-1]], 'Mouse position Y']  # 視点のy座標
                    mouse_start=[a, b]
                    c = input_mouse.at[input_mouse.index[click_index[-1]+after], 'Mouse position X']  # 視点のx座標
                    d = input_mouse.at[input_mouse.index[click_index[-1]+after], 'Mouse position Y']  # 視点のy座標
                    mouse_end=[c, d]
                    mouse_vec=np.array([c-a,d-b])
                    sac_start = input_mouse.at[input_mouse.index[click_index[-1]], 'Recording timestamp']  # サッカード開始時刻
                    ind=input_eye['Recording timestamp'].sub(sac_start).abs().idxmin()#最も近い時間の値
                    e = input_eye.at[input_eye.index[ind], 'Gaze point X']  # 視点のx座標
                    f = input_eye.at[input_eye.index[ind], 'Gaze point Y']  # 視点のy座標
                    eye_start=[e, f]
                    g = input_eye.at[input_eye.index[ind+after], 'Gaze point X']  # 視点のx座標
                    h = input_eye.at[input_eye.index[ind+after], 'Gaze point Y']  # 視点のy座標
                    eye_end=[g, h]
                    eye_vec=np.array([g-e,h-f])
                    naiseki=np.inner(eye_vec,mouse_vec)
                    theta=np.arccos(naiseki/(np.linalg.norm(eye_vec)*np.linalg.norm(mouse_vec)))
                    k_list.append(theta)
            kakudo.append(sum(k_list)/len(k_list))
    

            
print("-------------------pre--------------------")
plt.scatter(kakudo,pre)
#plt.xlim(0,100)
plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in kakudo]
# clf.fit(X2, pre) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
#ax.text(19.0, 0.6, '$ R^{2} $=' + str(round(r2_lin, 4)))
#plt.plot(df_x, y_lin_fit, color = '#000000', linewidth=0.5)
plt.xlabel("角度", fontname="MS Gothic")
plt.ylabel("事前自己効力感", fontname="MS Gothic")
plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, pre))
s1=pd.Series(kakudo)
s2=pd.Series(pre)
print(s1.corr(s2))

print("----------------post----------------")
plt.scatter(kakudo,post)
#plt.xlim(0,100)
plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in kakudo]
# clf.fit(X2, post) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
plt.xlabel("角度", fontname="MS Gothic")
plt.ylabel("事後自己効力感", fontname="MS Gothic")
plt.show()
# print("回帰係数= ", clf.coef_)
# print("切片= ", clf.intercept_)
# print("決定係数= ", clf.score(X2, post))
s1=pd.Series(kakudo)
s2=pd.Series(post)
print(s1.corr(s2))