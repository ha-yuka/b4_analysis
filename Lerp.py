# 欠損部分を線形補間する
# 欠損部分はデータフレームの特定の列のみに現れるので，それぞれの列に注目して補間する操作を繰り返す
import pandas as pd
NUM = [4, 6, 8, 10, 12]
f_num = 69
gfi = ''  # True : 欠損データ補間, False : 欠損データ除外
someone = ['tsubata/', 'mikiko/', 'kikuchirei/', 'takuno/', 'yamamoto/', 'aoki/', 'sasaki/', 'kobayashi/',
           'kunikata/', 'hirokawa/', 'ichihara/', 'maehashi/', 'muragi/']
file_name = ['syuchu', 'sogai', 'hirou']
day = ['01', '02']
slice_num = ['01', '02']
col_name = ['Recording timestamp', 'Computer timestamp', 'Eyetracker timestamp',
            'Event', 'Gaze point X', 'Gaze point Y', 'Pupil diameter left',
            'Pupil diameter right', 'Validity left', 'Validity right',
            'Eye movement type', 'Gaze event duration', 'Fixation point X', 'Fixation point Y']

for sm in someone:
    for fn in file_name:
        for dy in day:
            # ファイル読み込み
            if gfi:
                input_book = pd.ExcelFile('lerp invalid/gap fill in/' + sm + fn + dy + ' Data Export Trim.xlsx')
                print('lerp invalid/gap fill in/' + sm + fn + dy + ' Data Export Trim.xlsx')
            else:
                input_book = pd.ExcelFile('lerp invalid/' + sm + fn + dy + ' Data Export Trim.xlsx')
                print('lerp invalid/' + sm + fn + dy + ' Data Export Trim.xlsx')
            input_df = input_book.parse('Data')
            output_df = input_df.copy()  # 補間の必要がない列を保持するため，とりあえず全部コピーしておく

            if not input_df.empty:
                # 特定の列(cn)のみ線形補間し，output_dfの該当箇所を上書きする
                for cn in col_name:
                    # print(output_df[cn])
                    output_df[cn] = input_df[cn].interpolate().tolist() #補間
                    if not output_df[cn].equals(input_df[cn]):  # 出力用のDFが変更されたか一応確認
                        print('succeed')

            # ファイル書き出し
            if gfi == 'True':
                output_df.to_excel('gap fill in/lerp invalid/' + sm + fn + dy + ' Data Export Lerp.xlsx', sheet_name='Data', index=False)
                print('gap fill in/lerp invalid/' + sm + fn + dy + ' Data Export Lerp.xlsx')
            else:
                output_df.to_excel('lerp invalid/' + sm + fn + dy + ' Data Export Lerp.xlsx', sheet_name='Data', index=False)
                print('lerp invalid/' + sm + fn + dy + ' Data Export Lerp.xlsx')
            output_df = pd.DataFrame()

