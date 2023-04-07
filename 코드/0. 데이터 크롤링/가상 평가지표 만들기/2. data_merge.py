from glob import glob
import pandas as pd
from datetime import datetime

file_list = {"wl_1018662", "wl_1018680", "wl_1018683", "wl_1019630"} #해발표고El.m
df_list = []

for j in file_list:
    total=""
    file_list = glob(f'{j}*.xls')

    for i in file_list:
        with open(i, 'r', encoding='utf-8') as f:
            df = pd.read_html("".join(f.readlines()), encoding='utf-8')[0]
            if type(total) == str:
                total = df
            else:
                total = pd.concat([total, df], axis=0)
    
    total.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=False)
    total.drop(labels=total.columns.unique()[1], axis=1, inplace=True) # 수위
    total.drop(labels=total.columns.unique()[1], axis=1, inplace=True) # 유량
    total['시간'] = total['시간'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'))
    total = total.set_index('시간', drop=True)
    total[total.columns.unique()[0]] = total[total.columns.unique()[0]] * 100 - 0.3
    total = total.rename(columns={total.columns.unique()[0]:j})
    total.to_csv(f"{j}.csv")
    df_list.append(total)

results = ""
for k in df_list:
    if type(results) == str:
        results = k
    else:
        results = results.merge(k, left_index=True, right_index=True)
        
# 2022-06-01 00:00 ~ 2022-07-18 23:50 필터링
results = results.loc[f"2022-06-01 00:00":f"2022-07-18 23:50", :]
results = results.sort_values(by='시간')
print(results)
results.to_csv("평가지표데이터.csv")