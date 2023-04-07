import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import database
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pickle
import os
import datetime

# load_model = tf.keras.models.load_model('잠수교6시간후예측모델')
load_model = tf.keras.models.load_model('/root/web/haengju_model')
db = database.SqliteDb()
db.connect('/root/web/water.db')
# df = db.get_dataframe('water_collection')
df = db.get_dataframe('water_total')
# df.drop('index', axis=1, inplace=True)
df.drop('idx', axis=1, inplace=True)
df.set_index('ymdhm', inplace=True)


# 여기에 컬럼순서 변경 넣기
df = df[['rf_10184100', 'rf_10184110', 'rf_10184140', 'swl', 'inf', 'sfw', 'ecpc', 'tototf', 'tide_level', 'fw_1018662', 'fw_1018683', 'fw_1019630', 'wl_1018662', 'wl_1018680', 'wl_1018683', 'wl_1019630']]



if not os.path.exists('/root/web/scaler1_haengju.pkl') or not os.path.exists('/root/web/scaler2_haengju.pkl'):
    total_csv = pd.read_csv('/root/web/total.csv')
    total_csv.set_index('ymdhm', inplace=True)
    mms1 = StandardScaler()
    mms2 = StandardScaler()



    # 여기에 컬럼순서 변경 넣기
    total_csv = total_csv[['rf_10184100', 'rf_10184110', 'rf_10184140', 'swl', 'inf', 'sfw', 'ecpc', 'tototf', 'tide_level', 'fw_1018662', 'fw_1018683', 'fw_1019630', 'wl_1018662', 'wl_1018680', 'wl_1018683', 'wl_1019630']]




    mms1.fit(total_csv.iloc[:,:-1])
    mms2.fit(total_csv.iloc[:,-1:])
    pickle.dump(mms1, open('/root/web/scaler1_haengju.pkl','wb'))
    pickle.dump(mms2, open('/root/web/scaler2_haengju.pkl','wb'))
else:
    mms1 = pickle.load(open('/root/web/scaler1_haengju.pkl','rb'))
    mms2 = pickle.load(open('/root/web/scaler2_haengju.pkl','rb'))
dataset1 = mms1.transform(df.iloc[:,:-1])
dataset2 = mms2.transform(df.iloc[:,-1:])

dataset=np.concatenate([dataset1, dataset2], axis=1)
def multivariate_data(dataset, target, start_index, end_index, history_size, target_size, step, single_step = False):
    data = []
    labels = []
    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size
    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step)
        data.append(dataset[indices])
        if single_step:
            labels.append(target[i+target_size])
        else:
            labels.append(target[i:i+target_size])
    return np.array(data), np.array(labels)


past_history = 6*24*5 # 5일 데이터 = 6*24*5
future_target = 36 # 예측 n*10분 36일땐 6시간
STEP = 24 # 메모리가 부족할 땐 높게
BATCH_SIZE = 256
BUFFER_SIZE = 10000
EPOCHS2 = 5
EVALUATION_INTERVAL = 200
x_real = dataset[-6120:,]
x_real_array, _ = multivariate_data(x_real, x_real[:, -1], 0, None, past_history, future_target, STEP)

pred = load_model.predict(x_real_array)

# print(pred.shape)
# print(pred[-1])
# print(pred[-1].shape)

future_array = mms2.inverse_transform(pred[-1].reshape(-1,1))
fig = plt.figure(figsize=(7.5, 3.5))
# plt.plot(range(36), real, label='real')
now = datetime.datetime.now()
now = now.strftime("%y/%m/%d %H:%M")
plt.title(f'{now}에 예측한 수위 변화 그래프')
plt.plot(range(36), future_array, label='predict')
plt.xlabel('* 10min')
plt.ylabel('water level')
plt.legend()

new_content = ''
with open("/root/web/templates/dash_행주대교_form.html",'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        new_content += l
        if l.strip() == '<div class="right">':
            new_content += '\n\n'
            new_content += mpld3.fig_to_html(fig, figid='level')
            new_content += '\n\n'

with open("/root/web/templates/dash_행주대교.html", "w", encoding='utf-8') as f:
    f.write(new_content)
