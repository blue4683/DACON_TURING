from glob import glob
import pandas as pd

results=""
file_list = glob('*.csv')
df_list = []
for i in file_list:
    print(i)
    df = pd.read_csv(i)
    df = df.set_index('시간', drop=True)
    df = df.rename(columns={'강수량':i.split('_')[0]})
    df_list.append(df)
results = df_list[0].merge(df_list[1], left_index=True, right_index=True)
results = results.merge(df_list[2], left_index=True, right_index=True)
results.to_csv("3지역통합_강수량.csv")

