import pandas as pd
from datetime import datetime

# 필요한 데이터만 년도별로 따로 저장하기
# 대곡교, 진관교, 송정동
# 2012-05-01 00:00 ~ 2012-10-31 23:50
# ...
# 2022-05-01 00:00 ~ 2022-07-18 23:50

water_df = pd.read_csv("3지역통합_강수량.csv")
water_df['시간'] = water_df['시간'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'))
water_df = pd.read_csv("3지역통합_강수량.csv").set_index('시간', drop=True)

# 2012년 ~ 2021년 강수량
for n in range(2012, 2022):
    temp_df = water_df.loc[f"{n}-05-01 00:00":f"{n}-10-31 23:50", :]
    temp_df.to_csv(f"{n}_강수량.csv")

# 2022년 강수량
temp_df = water_df.loc[f"2022-05-01 00:00":f"2022-07-18 23:50", :]
temp_df.to_csv(f"2022_강수량.csv")