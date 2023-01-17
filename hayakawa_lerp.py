# 欠損部分を線形補間する
# 欠損部分はデータフレームの特定の列のみに現れるので，それぞれの列に注目して補間する操作を繰り返す
import pandas as pd
NUM = [4, 6, 8, 10, 12]
f_num = 69
gfi = ''  # True : 欠損データ補間, False : 欠損データ除外
someone = ['imahashi']#'tamura',,'watanabe','kawamura','kawasaki','kobayashi','maeda','motoyama','tamaru','nomura','ota','shigenawa','suzuki','tabata','yashiro'
file_name = ['n_iraira1']#,'n_iraira2','n_iraira3','n_iraira4','n_iraira5','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2'
#file_name=['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2']
day = ['01', '02']
slice_num = ['01', '02']
col_name = ['Recording timestamp','Event','Sensor','Gaze point X','Gaze point Y','Validity left','Validity right','Eye movement type','Mouse position X','Mouse position Y','Event value']

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

