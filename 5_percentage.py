import pandas as pd
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','nomura','ota','shigenawa','suzuki','tabata','tamaru','tamura','watanabe','yashiro']#,,'motoyama'
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2']
day = ['02']
around_30=[]
around_50=[]
around_100=[]
around_150=[]
around_200=[]
around_250=[]
pre=[]
post=[]
output_df=pd.DataFrame(columns=someone,index=file_name)
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#      
for sm in someone:
    for dy in day:
        for fn in file_name:
            print(sm,dy,fn)
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
            total=0 #視線データの数
            
            look_30=0
            look_50=0 #マウスの周りを見ていたデータの数
            look_100=0
            look_150=0
            look_200=0
            eye_index=0

            #各マウスデータについて，その時刻の直前に見ていた点とのユークリッド距離を算出

            input_mouse=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'mouse.csv', index_col=None)#マウスデータ読み込み
            drop_index=input_mouse.index[input_mouse['Event']=='MouseEvent']
            input_mouse=input_mouse.drop(drop_index)
            input_mouse = input_mouse.reset_index(drop=True)

            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視視線データ読み込み
            for data in input_mouse.itertuples():
                timestamp=data[1]#タイムスタンプ
                mouse_x=data[3]#マウスのx座標
                mouse_y=data[4]#マウスのy座標
                mouse_position=np.array((mouse_x,mouse_y))
                total=total+1

                if eye_index+1 == input_eye.shape[0]-1:
                    break
                pre_eye = input_eye.loc[eye_index,'Recording timestamp']
                post_eye = input_eye.loc[eye_index+1,'Recording timestamp']
                #print(input_eye.shape[0])

                while post_eye<timestamp:
                    eye_index=eye_index+1
                    if eye_index+1 == input_eye.shape[0]-1:
                        break
                    pre_eye = input_eye.loc[eye_index,'Recording timestamp']
                    post_eye = input_eye.loc[eye_index+1,'Recording timestamp']
                    #gaze_x = input_eye.loc[eye_index,'Gaze point Y']
                    #gaze_y = input_eye.loc[eye_index,'Gaze point Y']
                gaze_point = np.array((input_eye.loc[eye_index,'Gaze point X'],input_eye.loc[eye_index,'Gaze point Y']))
                dist = np.linalg.norm(mouse_position-gaze_point)#距離計算

                if dist<=30:
                    look_30=look_30+1
                if dist<=50:
                    look_50=look_50+1
                if dist<=100:
                    look_100=look_100+1
                if dist<=150:
                    look_150=look_150+1
                if dist<=200:
                    look_200=look_200+1
                # if dist<=250:
                #     look_250=look_250+1
                
            
            #print(fn,'percentage=',look/total)
            around_30.append((look_30/total)*100)
            around_50.append((look_50/total)*100)
            around_100.append((look_100/total)*100)
            around_150.append((look_150/total)*100)
            around_200.append((look_200/total)*100)
            #around_250.append((look_250/total)*100)
            #print((look_100/total)*100)
            output_df.loc[fn,sm]=(look_30/total)*100

output_df.to_excel("./around_30.xlsx")

# plt.scatter(around_100,pre)
# plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in around_100]
# clf.fit(X2, pre) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# plt.xlabel("カーソルの周辺100ピクセルを見ている割合", fontname="MS Gothic")
# plt.ylabel("事前自己効力感", fontname="MS Gothic")
# plt.show()

# print("----------pre----------")
# print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
# print("切片= ", '{:.3f}'.format (clf.intercept_))
# print("決定係数= ", '{:.3f}'.format (clf.score(X2, pre)))
# s1=pd.Series(around_30)
# s2=pd.Series(pre)
# print("30:","相関係数= ",'{:.3f}'.format (s1.corr(s2))) 
# s1=pd.Series(around_50)
# s2=pd.Series(pre)
# print("50:","相関係数= ",'{:.3f}'.format (s1.corr(s2))) 
# s1=pd.Series(around_100)
# s2=pd.Series(pre)
# print("100:","相関係数= ",'{:.3f}'.format (s1.corr(s2))) 
# s1=pd.Series(around_150)
# s2=pd.Series(pre)
# print("150:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_200)
# s2=pd.Series(pre)
# print("200:","相関係数= ",'{:.3f}'.format (s1.corr(s2))) 
# s1=pd.Series(around_250)
# s2=pd.Series(pre)
# print("250:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))


# print("----------post----------")
# plt.scatter(around_100,post)
# plt.xlim(0,100)
# plt.ylim(0,100)
# clf = linear_model.LinearRegression()
# X2 = [[x] for x in around_100]
# clf.fit(X2, post) # 予測モデルを作成
# plt.plot(X2, clf.predict(X2))
# plt.xlabel("カーソルの周辺100ピクセルを見ている割合", fontname="MS Gothic")
# plt.ylabel("事後自己効力感", fontname="MS Gothic")
# plt.show()
# print("回帰係数=", '{:.3f}'.format (clf.coef_[0]))
# print("切片= ", '{:.3f}'.format (clf.intercept_))
# print("決定係数= ", '{:.3f}'.format (clf.score(X2, post)))
# s1=pd.Series(around_30)
# s2=pd.Series(post)
# print("30:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_50)
# s2=pd.Series(post)
# print("50:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_100)
# s2=pd.Series(post)
# print("100:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_150)
# s2=pd.Series(post)
# print("150:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_200)
# s2=pd.Series(post)
# print("200:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
# s1=pd.Series(around_250)
# s2=pd.Series(post)
# print("250:","相関係数= ",'{:.3f}'.format (s1.corr(s2)))
