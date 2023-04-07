'''
# 평가 규칙
평가 산식: RMSE / R_Squared_Score
R_Squared_Score <= 0인 경우 999출력
각 다리의 예측된 수위에 대한 점수를 평균하여 리더보드에 표시
'''
# 테스트 정답 데이터: 평가지표데이터.csv
# 평가 산식: RMSE / R_Squared_Score
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

pred = pd.read_csv("data+1안밀고한결과값_한별.csv")
target = pd.read_csv("평가지표데이터.csv")

print('train rmse score: ', mean_squared_error(target, pred)**0.5)
# print('val rmse score:', mean_squared_error(test_target, pred_val)**0.5)