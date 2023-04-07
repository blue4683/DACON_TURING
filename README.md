> # [2022 DACON - 팔당댐 방류로 인한 한강 주요다리 수위 예측](https://dacon.io/competitions/official/235949/overview/description)

## 개요
- 기간 : 2022.08.09 ~ 2022.08.29
- 언어 : `Python==3.7.4`
- 제출 : [사이트](https://dacon.io/competitions/official/235949/overview/description)

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