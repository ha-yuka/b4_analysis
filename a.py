import pandas as pd

input_eye=pd.read_csv('exp_data/'+'imahashi'+'01'+'/remove/' + 'iraira1-1'+'_'+ 'eye_all.csv', index_col=None)#マウスデータ読み込み
output_eye = input_eye.copy()  # 補間の必要がない列を保持するため，とりあえず全部コピーしておく
output_eye['Gaze point X'] = input_eye['Gaze point X'].interpolate().tolist() #補間
output_eye['Gaze point Y'] = input_eye['Gaze point Y'].interpolate().tolist() #補間
if not output_eye['Gaze point X'].equals(input_eye['Gaze point X']):  # 出力用のDFが変更されたか一応確認
        print('x-succeed')
if not output_eye['Gaze point Y'].equals(input_eye['Gaze point Y']):  # 出力用のDFが変更されたか一応確認
        print('y-succeed')

output_eye.to_csv('exp_data/'+'imahashi'+'01'+'/remove/' + 'iraira1-1'+'_'+ 'lerp.csv',  index=False)#ファイルに出力
print('exp_data/'+'imahashi'+'01'+'/remove/' + 'iraira1-1'+'_'+ 'lerp.csv')
