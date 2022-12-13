import pandas as pd

key_num = 3  # 削除する前後3s
del_index = []  # 前後3s間の行番号を格納
end_num = 10  # 削除する作業終了直前の10s
someone = ['kawamura/']
file_name = ['iraira1-1']
data_kind=['eye','mouse','obj']
day = ['01']
gfi = '' #invalid入れるかどうか


input_obj=pd.read_csv('data/' + 'kawamura'+ '01/' +'obj/'+ 'iraira1-1.csv')#ファイルの読み込み
print(input_obj.head(1)) #開始時
#print(input_obj.tail(1)) #終了時
#input_eye=pd.ExcelFile('data/' + 'kawamura'+ '01/' + 'eyedata/'+'kawamura'+'01 '+'iraira1-1.xlsx')#ファイルの読み込み

"""
text_start_index = input_df.index[(input_df['Event'] == 'Eye tracker Calibration end')].tolist()
            text_df = input_df.drop(range(text_start_index[0] + 2))
"""
"""
input_eye=pd.ExcelFile('data/' + 'kawamura'+ '01/' + 'mousedata/'+'kawamura'+'01'+'iraira1-1.csv')#ファイルの読み込み
"""
"""
for sm in someone:
    for fn in file_name:
        for dy in day:
            # 読み込み
            if gfi == 'True':
                input_book = pd.ExcelFile('Data Export - ' + sm + dy +'/'  + ' Data Export.xlsx')#ファイルの読み込み
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
"""
# print(df)
