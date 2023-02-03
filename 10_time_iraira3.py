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

someone = ['imahashi','kawamura','kawasaki','kobayashi','maeda','nomura','ota','shigenawa','suzuki','tabata','tamaru','tamura','watanabe','yashiro']
file_name = ['n_iraira3','iraira3-1','iraira3-2']
day = ['02']#, '02'
pre=[]
post=[]
col_name=['Recording timestamp','pre_area','post_area']

output_df=pd.read_excel("./time_gap.xlsx", index_col=0)
area=100
wide=1880
high=1040
width=1920
hight=1080
w=100
aoi_1=[width-(20+wide/3-w+area),(20+w-area),width-(20+wide/3-w-area),(20+w+area)]
aoi_2=[width-(20+wide/3-w+area),(20+high/2-w-area),width-(20+wide/3-w-area),(20+high/2-w+area)]
aoi_3=[width-(20+w+area),(20+high/2-area),width-(20+w-area),(20+high/2+area)]
aoi_4=[width-(20+w+area),(20+high-w-area),width-(20+w-area),(20+high-w+area)]
aoi_5=[width-(20+wide*2/3-w*2+area),(20+high-w-area),width-(20+wide*2/3-w*2-area),(20+high-w+area)]
aoi_6=[width-(20+wide*2/3-w*2+area),(20+high/2+w-area),width-(20+wide*2/3-w*2-area),(20+high/2+w+area)]
aoi_7=[width-(20+wide/3+w*2+area),(20+high/2-area),width-(20+wide/3+w*2-area),(20+high/2+area)]
aoi_8=[width-(20+wide/3+w*2+area),(20+w-area),width-(20+wide/3+w*2-area),(20+w+area)]
aoi_9=[width-(20+wide*2/3+area),(20+w-area),width-(20+wide*2/3-area),(20+w+area)]
aoi_10=[width-(20+wide*2/3+w+area),(20+high/2-area),width-(20+wide*2/3+w-area),(20+high/2+area)]
aoi_11=[width-(20+wide-w+area),(20+high/2+w-area),width-(20+wide-w-area),(20+high/2+w+area)]
aoi_12=[width-(20+wide-w+area),(20+high-w-area),width-(20+wide-w-area),(20+high-w+area)]
aoi_13=[width-(20+wide*2/3+w/2+area),(40+high-2*area),width-(20+wide*2/3+w/2-area),(high+40)]

time_gap=[]
#========================アンケート結果読み込み=====================#
task01=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
task02=pd.read_excel('task02.xlsx',index_col=None)#ファイルの読み込み
#=================================================================#
for sm in someone:
    for dy in day:
        for fn in file_name:
            print(sm,dy,fn)
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
            t_obj=0
            t_0_obj=0
            for i in range(0,len(input_obj)-1):#オブジェクトの位置1行ずつ見ていく
                x=input_obj.loc[i,'Position X']
                y=input_obj.loc[i,'Position Y']
                t_0_obj=t_obj
                if aoi_1[0]<=x<=aoi_1[2] and aoi_1[1]<=y<=aoi_1[3] and t_obj!=1:#aoi1
                    t_obj=1 
                elif aoi_2[0]<=x<=aoi_2[2] and aoi_2[1]<=y<=aoi_2[3]and t_obj!=2:
                    t_obj=2
                elif aoi_3[0]<=x<=aoi_3[2] and aoi_3[1]<=y<=aoi_3[3]and t_obj!=3:
                    t_obj=3
                elif aoi_4[0]<=x<=aoi_4[2] and aoi_4[1]<=y<=aoi_4[3]and t_obj!=4:
                    t_obj=4
                elif aoi_5[0]<=x<=aoi_5[2] and aoi_5[1]<=y<=aoi_5[3]and t_obj!=5:
                    t_obj=5
                elif aoi_6[0]<=x<=aoi_6[2] and aoi_6[1]<=y<=aoi_6[3]and t_obj!=6:
                    t_obj=6
                elif aoi_7[0]<=x<=aoi_7[2] and aoi_7[1]<=y<=aoi_7[3]and t_obj!=7:
                    t_obj=7
                elif aoi_8[0]<=x<=aoi_8[2] and aoi_8[1]<=y<=aoi_8[3]and t_obj!=8:
                    t_obj=8
                elif aoi_9[0]<=x<=aoi_9[2] and aoi_9[1]<=y<=aoi_9[3]and t_obj!=9:
                    t_obj=9
                elif aoi_10[0]<=x<=aoi_10[2] and aoi_10[1]<=y<=aoi_10[3]and t_obj!=10:
                    t_obj=10
                elif aoi_11[0]<=x<=aoi_11[2] and aoi_11[1]<=y<=aoi_11[3]and t_obj!=11:
                    t_obj=11
                elif aoi_12[0]<=x<=aoi_12[2] and aoi_12[1]<=y<=aoi_12[3]and t_obj!=12:
                    t_obj=12
                elif aoi_13[0]<=x<=aoi_13[2] and aoi_13[1]<=y<=aoi_13[3]and t_obj!=13:
                    t_obj=13
                
                if t_0_obj!=t_obj:#AOIからAOIへの遷移
                    mouse_t.append([input_obj.loc[i,'Recording timestamp'],t_0_obj,t_obj])
                    #print(obj, obj_1,t_obj,t_1_obj)
            mouse_df=pd.DataFrame(mouse_t,columns=col_name)
            print("===============================")
            #print(mouse_df)

            # #=======================視線の移動============================#
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv', index_col=None)#視線データ
            t_eye=0
            t_0_eye=0
            #['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type']
            for i in range(0,len(input_eye)-1):#オブジェクトの位置1行ずつ見ていく
                x=input_eye.loc[i,'Gaze point X']
                y=input_eye.loc[i,'Gaze point Y']
                t_0_eye=t_eye
                if aoi_1[0]<=x<=aoi_1[2] and aoi_1[1]<=y<=aoi_1[3] and t_eye!=1:#aoi1
                    t_eye=1 
                elif aoi_2[0]<=x<=aoi_2[2] and aoi_2[1]<=y<=aoi_2[3]and t_eye!=2:
                    t_eye=2
                elif aoi_3[0]<=x<=aoi_3[2] and aoi_3[1]<=y<=aoi_3[3]and t_eye!=3:
                    t_eye=3
                elif aoi_4[0]<=x<=aoi_4[2] and aoi_4[1]<=y<=aoi_4[3]and t_eye!=4:
                    t_eye=4
                elif aoi_5[0]<=x<=aoi_5[2] and aoi_5[1]<=y<=aoi_5[3]and t_eye!=5:
                    t_eye=5
                elif aoi_6[0]<=x<=aoi_6[2] and aoi_6[1]<=y<=aoi_6[3]and t_eye!=6:
                    t_eye=6
                elif aoi_7[0]<=x<=aoi_7[2] and aoi_7[1]<=y<=aoi_7[3]and t_eye!=7:
                    t_eye=7
                elif aoi_8[0]<=x<=aoi_8[2] and aoi_8[1]<=y<=aoi_8[3]and t_eye!=8:
                    t_eye=8
                elif aoi_9[0]<=x<=aoi_9[2] and aoi_9[1]<=y<=aoi_9[3]and t_eye!=9:
                    t_eye=9
                elif aoi_10[0]<=x<=aoi_10[2] and aoi_10[1]<=y<=aoi_10[3]and t_eye!=10:
                    t_eye=10
                elif aoi_11[0]<=x<=aoi_11[2] and aoi_11[1]<=y<=aoi_11[3]and t_eye!=11:
                    t_eye=11
                elif aoi_12[0]<=x<=aoi_12[2] and aoi_12[1]<=y<=aoi_12[3]and t_eye!=12:
                    t_eye=12
                elif aoi_13[0]<=x<=aoi_13[2] and aoi_13[1]<=y<=aoi_13[3]and t_eye!=13:
                    t_eye=13
                
                if t_0_eye!=t_eye:#AOIからAOIへの遷移
                    eye_t.append([input_eye.loc[i,'Recording timestamp'],t_0_eye,t_eye])
            eye_df=pd.DataFrame(eye_t,columns=col_name)
            #print(eye_df)
            
            # #==================時間差算出==================#
            to_one_index = eye_df.index[(eye_df['post_area'] == 1)].tolist()#→1
            to_one_df=eye_df.loc[to_one_index,]
            to_two_index = eye_df.index[(eye_df['post_area'] == 2)].tolist()#→2
            to_two_df=eye_df.loc[to_two_index,]
            to_three_index = eye_df.index[(eye_df['post_area'] == 3)].tolist()#→3
            to_three_df=eye_df.loc[to_three_index,]

            to_four_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 4)].tolist(),]#4
            to_five_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 5)].tolist(),]#→5
            to_six_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 6)].tolist(),]#→6
            to_seven_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 7)].tolist(),]#→7
            to_eight_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 8)].tolist(),]#→8
            to_nine_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 9)].tolist(),]#→9
            to_ten_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 10)].tolist(),]#→10
            to_eleven_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 11)].tolist(),]#→11
            to_twelve_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 12)].tolist(),]#→12
            to_13_df=eye_df.loc[eye_df.index[(eye_df['post_area'] == 13)].tolist(),]#→13
            # print("==========================")
            # print(two_one_df)
            # print(one_zero_df)
            # print(zero_one_df)
            # print(one_two_df)
            for i in range(0,len(mouse_df)):
                post_a=mouse_df.loc[i,'post_area']
                t=mouse_df.loc[i,'Recording timestamp']
                if post_a==1 and len(to_one_df)!=0:
                    u=to_one_df.loc[to_one_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==2 and len(to_two_df)!=0:
                    u=to_two_df.loc[to_two_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==3 and len(to_three_df)!=0:
                    u=to_three_df.loc[to_three_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==4 and len(to_four_df)!=0:
                    u=to_four_df.loc[to_four_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==5 and len(to_five_df)!=0:
                    u=to_five_df.loc[to_five_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==6 and len(to_six_df)!=0:
                    u=to_six_df.loc[to_six_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==7 and len(to_seven_df)!=0:
                    u=to_seven_df.loc[to_seven_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==8 and len(to_eight_df)!=0:
                    u=to_eight_df.loc[to_eight_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==9 and len(to_nine_df)!=0:
                    u=to_nine_df.loc[to_nine_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==10 and len(to_ten_df)!=0:
                    u=to_ten_df.loc[to_ten_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==11 and len(to_eleven_df)!=0:
                    u=to_eleven_df.loc[to_eleven_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==12 and len(to_twelve_df)!=0:
                    u=to_twelve_df.loc[to_twelve_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                elif post_a==13 and len(to_13_df)!=0:
                    u=to_13_df.loc[to_13_df['Recording timestamp'].sub(t).abs().idxmin(),'Recording timestamp']
                if abs(t-u)<=1:
                    sub_gap.append(t-u)    
            time_gap.append(sum(sub_gap)/len(sub_gap))  # 平均時間差
            print(len(sub_gap))
            #print(sub_gap,sum(sub_gap)/len(sub_gap))
            #print(sm,dy,fn)
            output_df.loc[fn,sm]=sum(sub_gap)/len(sub_gap)

output_df.to_excel("./time_gap.xlsx")

# dnarray = np.array([time_gap,pre,post])
# df=pd.DataFrame(dnarray)
# df.to_csv("./timegap.csv",mode='a',header=False,index=False)