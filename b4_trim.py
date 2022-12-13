import pandas as pd
key_num = 3  # 削除する前後3s
del_index = []  # 前後3s間の行番号を格納
end_num = 10  # 削除する作業終了直前の10s
someone = ['watanabe/','suzuki/','shigenawa/','maeda/','kobayasi/','kawasaki/','tamura/','tamaru/','nomura/','motoyama/','ota/','kawamura/','imahashi/','yashiro/','tabata/']
file_name = ['n_puzzle1', 'n_puzzle2', 'n_puzzle3','n_puzzle4','n_puzzle5','puzzle1-1','puzzle1-2','puzzle2-1','puzzle2-2','puzzle3-1','puzzle3-2','puzzle4-1','puzzle4-2','puzzle5-1','puzzle5-2','iraira1-1','iraira1-2','iraira2-1','iraira2-2','iraira3-1','iraira3-2','iraira4-1','iraira4-2','iraira5-1','iraira5-2',]
day = ['01', '02']
gfi = ''

for sm in someone:
    for fn in file_name:
        for dy in day:
            # 読み込み
            if gfi == 'True':
                input_book = pd.ExcelFile('gap fill in/' + sm + fn + dy + ' Data Export.xlsx')
            else:
                input_book = pd.ExcelFile('./00/ignore invalid/' + sm + fn + dy + ' Data Export.xlsx')
            input_df = input_book.parse('Data')

            # textstartまでを削除
            text_start_index = input_df.index[(input_df['Event'] == 'Eye tracker Calibration end')].tolist()
            text_df = input_df.drop(range(text_start_index[0] + 2))

            # 必要な列を抽出
            df = text_df.loc[:,['Recording timestamp','Computer timestamp','Eyetracker timestamp',
                           'Event','Gaze point X','Gaze point Y']]
            df = df.reset_index(drop=True)

            # keyboard操作の前後と作業開始後、終了前の10sを削除
            # 全てのdel_indexを1列のリストにして、ループ後に一括削除する

            # 作業開始直後の3sをdel_indexに追加
            del_index.extend(df.index[df['Recording timestamp'] <= df.iat[0, 0] + key_num * 1000000].tolist())

            # keyboardEventの前後3sをdel_indexに追加
            # key_index = df.index[df['Event'] == #'KeyboardEvent'].tolist()
            # for i in key_index[0:-2]:
            #     key_time = df.iat[i, 0]
            #     del_index.extend(df.index[(df['Recording # timestamp'] >= key_time - key_num * 1000000) & (
            #                 df['Recording timestamp'] <= # key_time + key_num * 1000000)].tolist())

            # 作業終了時のkeyboardEventの前10sをdei_indexに追加
            # key_time = df.iat[key_index[-1], 0]
            # del_index.extend(df.index[(df['Recording # timestamp'] >= key_time - end_num * 1000000) & (
            #                 df['Recording timestamp'] <= # key_time + end_num * 1000000)].tolist())

            # del_indexの行を一括削除
            df = df.drop(index=df.index[list(dict.fromkeys(del_index))])  # list(dict.fromkeys())で，del_index内の重複を削除
            # 欠損データを含む行を削除
            # df = df.dropna(subset=['Gaze point X', 'Gaze point Y', 'Pupil diameter left', 'Pupil diameter right']) # ここを実行する場合：delete invalid
            df = df.reset_index(drop=True)

            # ファイル書き出し
            if gfi == 'True':
                df.to_excel('delete invalid/gap fill in/' + sm + fn + dy + ' Data Export Trim.xlsx', sheet_name='Data', index=False)
            else:
                df.to_excel('./00/ignore invalid/' + sm + fn + dy + ' Data Export Trim.xlsx', sheet_name='Data', index=False)
            df = pd.DataFrame()
            del_index.clear()
# print(df)
