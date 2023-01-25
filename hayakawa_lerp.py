# 欠損部分を線形補間する
# 欠損部分はデータフレームの特定の列のみに現れるので，それぞれの列に注目して補間する操作を繰り返す
import pandas as pd


someone = ['imahashi','watanabe']
#someone=['tamura']'imahashi','watanabe','kawamura',,'kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro''kawasaki'
file_name = ['n_iraira1','n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','iraira5-1','iraira5-2','puzzle5-1','puzzle5-2']
day = ['01','02']#,
#col_name = ['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type','Mouse position X','Mouse position Y','Event value']

for sm in someone:
    for fn in file_name:
        for dy in day:
            # ファイル読み込み
            input_eye=pd.read_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv', index_col=None)#マウスデータ読み込み
            print('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'eye_all.csv')
            output_eye = input_eye.copy()  # 補間の必要がない列を保持するため，とりあえず全部コピーしておく
            output_eye['Gaze point X'] = input_eye['Gaze point X'].interpolate().tolist() #補間
            output_eye['Gaze point Y'] = input_eye['Gaze point Y'].interpolate().tolist() #補間

            output_eye.to_csv('exp_data/'+sm+dy+'/remove/' + fn+'_'+ 'lerp.csv',  index=False)#ファイルに出力

