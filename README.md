> # [DACON - 팔당댐 방류로 인한 한강 주요다리 수위 예측](https://dacon.io/competitions/official/235949/overview/description)

## 개요
- 기간 : 2022.08.09 ~ 2022.08.29
- 언어 : `Python==3.7.4`
- 제출 : [사이트](https://dacon.io/competitions/official/235949/overview/description)

## 목표
- 2012년 5월 1일 00시 00분 ~ 2022년 5월 31일 23시 50분(연도별 구간 = 5월 1일 ~ 10월 31일)의 강수량(대곡교, 진관교, 송정동), 팔당댐(현재 수위, 유입량, 저수량, 공용량, 총 방류량), 강화대교 조위, 청담대교,잠수교,한강대교,행주대교(수위, 유량) 데이터를 이용한다.
- 2022년 6월 1일 00시 00분 ~ 2022년 7월 18일 23시 50분의 청담대교·잠수교·한강대교·행주대교 수위를 예측한다.

## 추가 목표
- 매 시각의 데이터를 크롤링해 주기적인 수위예측 결과를 웹사이트에 올린다.

## 팀원
- 김주영(팀장) : 프로젝트 총괄, 문서 정리, 기준선 코드 작성(데이콘 유저 공유 코드), 데이터 분석, 수치형 데이터 범주화, 머신러닝 모델 학습(GradientBoost, RandomForest, Xgboost, Arima)
- 안경준 : 기준선 코드 작성(데이콘 제공 기준선 코드, 데이콘 유저 공유 코드), 램(RAM) 메모리를 적게 사용하는 코드 구상, 데이터 분석, 딥러닝 모델 학습(LSTM, 딥러닝 모델 학습 방식 구상)
- 이한별 : 기준선 코드 작성(데이콘 제공 기준선 코드, 전반적인 코드 정리 및 개선), 램(RAM) 메모리를 적게 사용하는 코드 구현, 데이터 분석, 추가 기능 구현(추가 데이터 수집을 위한 웹 크롤링, 자체 평가지표, 딥러닝 모델 epoch 별 가중치 저장 및 활용), 웹용 모델 작성, 머신러닝 모델 튜닝, 웹페이지 작성

## 개발 환경
- Google Colab & VSCode
- Jupyter Notebook
- Notion(결과 정리)

### 크롤링 & 모델링
```
tensorflow-cpu==2.9.1
sklearn==1.0.2
h5py==3.7.0
joblib==1.1.0
keras==2.9.0
matplotlib==3.5.3
numpy==1.21.6
pandas==1.3.5
playwright==1.25.2
requests==2.28.1
databases==0.6.1
```

### 웹
```
fastapi==0.79.0
Jinja2==3.1.2
uvicorn==0.18.2
requests==2.28.1
plot.ly==5.10.0
mpld3==0.5.8
tensorflow-cpu==2.9.1
sklearn==1.0.2
h5py==3.7.0
joblib==1.1.0
keras==2.9.0
matplotlib==3.5.3
numpy==1.21.6
pandas==1.3.5
playwright==1.25.2
databases==0.6.1
```

## 진행

### 분석 방법 결정
- 문제를 해결하기 위해 데이터를 구하기 쉬운 한강 주요다리 4개로 범위를 축소했다. 다리의 수위 데이터는 한강홍수통제소에서 구할 수 있었다.
- 수위를 예측하기 위한 변수로 각 다리의 ‘유량과 수위’를 넣었으며, 한강의 수위에 영향을 끼치는 상류의 댐인 ‘팔당댐의 주요 지표’(수위, 유입량, 저수량, 공용량, 방류량)와 한강과 바다가 만나 간조 만조의 수위 차가 심한 강화대교의 ‘조위’를 변수로 선정하였다. 추가로 대곡교, 진관교, 송정동의 강수량도 추가하였다.
- 시계열 분석을 통해 문제를 해결하려 했으나, 회귀 분석으로도 충분한 목표달성이 되리라 생각했고, 약 26만 건의 데이터양이 딥러닝으로만 처리하기에는 애매한 양이었기 때문에 머신러닝과 딥러닝으로 각각 모델을 만들어 보기로 하였다.

### 데이터 준비
1. 데이터 크롤링
- 2012년 5월 1일 ~ 2022년 5월 31일 데이터(water_data) 불러오기(팔당댐 관련 데이터, 조위, 수위 등) (연도별 데이터 기간 = 5월 1일 00시 00분 ~ 10월 31일 23시 50분) [한강홍수통제소 제공]
- 2012년 5월 1일 ~ 2022년 5월 31일 강수량 데이터(rf_data) 불러오기(연도별 데이터 기간 = 5월 1일 00시 00분 ~ 10월 31일 23시 50분) [한강홍수통제소 제공]
- 2012년 5월 1일 ~ 2022년 5월 31일 강화대교 조위 불러오기 [국립해양조사원 바다누리 해양 정보 서비스]
- 2022년 6월 1일 00시 00분 이후의 4개 교량의 수위 데이터 크롤링 [한강홍수통제소 제공]
- 위의 데이터를 '[데이콘](http://www.hrfco.go.kr/)에서 다운로드', '한강홍수통제소에서 크롤링', '[국립해양조사원 바다누리 해양 정보 서비스 OPENAPI](http://www.khoa.go.kr/oceangrid/khoa/intro.do)를 이용한 파싱'을 통해 취합했다.

2. 데이터 전처리
- 2012년 5월 1일 00시 00분 ~ 2022년 5월 31일 23시 50분 기간의 water_data와 rf_data의 인덱스 datetime화 후 시간순으로 데이터 정렬
- 인덱스를 기준으로 water_data와 rf_data를 concat()
- concat한 데이터를 train 데이터와 test 데이터로 분리 후 타겟 값(4개 다리의 수위) 분리
- 결측치를 각 데이터의 평균으로 채움(test 데이터는 train 데이터의 평균으로 채움)
- 강수량 데이터 범주화 (3개 장소의 강수량을 합쳐 강수량이 0mm, 0mm 초과 10mm 이하, 10mm 초과의 3구간으로 나눠 각각 0, 1, 2를 부여한 컬럼 생성)
- DL 학습을 위해 MinMaxScaler를 통해 데이터 스케일링(test 데이터는 train 데이터로 fit한 스케일러 사용)
- 팔당댐과 다리 간의 지리적인 거리 차를 고려한 데이터 행 조절(팔당댐이 방류를 시작한 순간 모든 다리의 수위가 즉시 상승하는 것은 아니다.)
- 유량과 수위의 상관관계를 추정한 추가 컬럼 생성
- 잠수교의 유량이 한강홍수통제소에 제시되어 있으나 실제로는 측정하지 않는 값이기 때문에 제거
- 팔당댐의 유입량과 청담대교의 유량은 가끔 센서의 이상으로 0으로 표시되기 때문에 0을 결측값으로 변화시켜 그 값을 앞뒤 전후로 보간한다.
- DL 손실함수로 데이콘 자체 평가지표(rmse / r2_score) 제작
- 10분 뒤의 수위를 예측하는 것이 목표였으므로, row의 위치를 재조정하여 데이터는 [그림-2]와 같이 처리하고, target은 각 다리의 수위 1개 또는 다리 4를 동시에 예측하게 하였다.

### ML 설계
- 여러 가지 ML모델을 시험해 본 결과, randomforest 모델이 가장 좋은 결과를 내는 것으로 초기에 판단하여 randomforest 모델로 고정하고 기타 파라미터와 데이터 처리를 중점으로 작업을 진행했다.
- baseline 모델을 만든 뒤, 얻은 결과는 평가지표 기준 4점대였다.
- ML 모델 RandomForest(n_jobs = -1, random_state = 42) 설계 (같은 조건(전처리한 데이터)에서 가장 좋은 성능)
- GridSearchCV로 n_estimators = 250, cv = KFold(n_splits=2, shuffle=True) 파라미터 선정 후 사용하였다.
- 수위에 가장 영향을 많이 끼치는 지표를 features_importance를 통해 보면 10분 전의 해당 다리의 수위, 유량, 팔당댐의 방류량, 강화대교의 조위가 영향을 많이 끼침을 알 수 있었고, 특히 팔당댐과 강화대교의 지리적 거리가 다리마다 차이나는 것을 해당 컬럼의 행 위치를 조정함으로써 최적화를 시키려 하였다.

### DL 설계
1. 기본모델 구성
- 머신러닝은 회귀를 사용하여 문제를 해결했지만, 딥러닝은 시계열 방식을 도입해 보기로 했다.
- 4개 층을 쌓는 것이 가장 좋은 효과를 내었으며, 구성된 모델의 정보는 다음과 같다.
- 모델을 위와 같이 고정해 놓고 learning rate와 기타 파라미터(Dropout, activation, optimizer, epoch)를 변경해 가며 학습을 시행했다.
- loss function을 데이콘에서 리더보드 평가 기준으로 정한 RMSE/R2_Score로 변경해 학습을 수행했다.
- 학습 진행 중 지표가 좋게 나오는 가중치를 저장하여 데이콘에 제출하였다. 약 1.2 점수를 기록.

2. 웹 서비스용 모델 설계
- 10분 뒤의 수위를 예측하는 기본모델과는 달리 웹용으로 서비스할 모델은 10분 이상의 수위를 예측해야 했다. 그래서 다른 모델을 구성해야 했다.
- 특히 일정 시간 이후의 수위를 예측하는 것은 예측 바로 직전의 유량 및 조위와 같은 데이터를 주지 않기 때문에 정확도가 다소 떨어지는 것을 감수해야 했고, 약 4시간 뒤의 데이터까지 유의미한 결과를 내었다.
- 4개 층을 쌓는 것이 가장 좋은 효과를 내었으며, 양방향(Bidirectional) LSTM 층을 활용하여 설계하였다.

### 웹 설계
- 웹페이지를 Nginx + fastapi를 이용하여 python과 html로 구성하였고, 그에 필요한 수위 변화 자료를 백그라운드 서비스로 5분마다 각 사이트에서 크롤링해 구현하였다.
- 서버는 GPU가 지원되지 않기 때문에 tensorflow-cpu를 이용하였다.
- 서비스로 5분마다 주기적으로 돌아가는 크롤러가 SQL에 저장하고, 비주기적으로 그 결과를 그래프로 만들고 mpld3를 이용해 html로 변환해 보여주었다.

## 참고
- Myungjin Lee; Hung Soo Kim; Jaewon Kwak; Jongsung Kim; Soojun Kim, 2022, Chaotic Features of Decomposed Time Series from Tidal River Water Level
- 건설교통부 한강홍수통제소, 2000, 한강(하류) 및 임진강 유역 유량측정 보고서
- 박석환, 2019, 딥러닝을 이용한 도심지 수위예측 : 도림천 유역 대상
- K-water 융합연구원, 2018, K-water 수위-유량 관계곡선식 산정 SW(K-HQ)