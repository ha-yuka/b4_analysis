import pandas as pd

input=pd.read_excel('task01.xlsx',index_col=None)#ファイルの読み込み
index=(input.index[input['被験者']=='imahashi'])[0]
print(input['被験者']=='imahashi')
pre='iraira1-1'+'_pre'
print(len(input))