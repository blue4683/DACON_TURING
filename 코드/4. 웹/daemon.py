"""
### 자료이용정책
* 환경부: 저작권법 제24조의2에 따라 환경부에서 저작재산권의 전부를 보유한 저작물의 경우에는 별도의 이용허락 없이 자유이용이 가능(팔당댐 및 다리의 자료)
* 해양수산부: openapi로 수집가능한 자료의 자유로운 이용 가능(강화대교 조위)
"""

"""
### 수집할 자료
강화대교 조위
https://www.khoa.go.kr/api/oceangrid/tideObs/search.do?ServiceKey=kH9DXri8W9Ny6w0onLeuqw==&ObsCode=DT_0032&Date=20220824&ResultType=json


팔당댐 현재수위, 유입량, 총 방류량
http://www.hrfco.go.kr/popup/damPopup.do?Obscd=1017310&Obsnm= 팔당댐 &Edt=2022-08-24 15:40

팔당댐 저수량, 공용량
http://www.hrfco.go.kr/sumun/damList.do


청담대교 수위, 유량
http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018662&Sdt=2022-08-24%2015:40&Edt=2022-08-24%2015:40&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%B2%AD%EB%8B%B4%EB%8C%80%EA%B5%90)

잠수교 수위
http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018680&Sdt=2022-08-24%2015:40&Edt=2022-08-24%2015:40&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%9E%A0%EC%88%98%EA%B5%90)

한강대교 수위, 유량
http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018683&Sdt=2022-08-24%2015:40&Edt=2022-08-24%2015:40&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%95%9C%EA%B0%95%EB%8C%80%EA%B5%90)

행주대교 수위, 유량
http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1019630&Sdt=2022-08-24%2015:40&Edt=2022-08-24%2015:40&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%96%89%EC%A3%BC%EB%8C%80%EA%B5%90)

대곡교 강수량
http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184100&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EB%8C%80%EA%B3%A1%EA%B5%90)&Edt=2022-08-24%2015:40

진관교 강수량
http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184110&Obsnm=%EB%82%A8%EC%96%91%EC%A3%BC%EC%8B%9C(%EC%A7%84%EA%B4%80%EA%B5%90)&Edt=2022-08-24%2015:40

송정동 강수량
http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184140&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%86%A1%EC%A0%95%EB%8F%99)&Edt=2022-08-24%2015:40
"""

import time
import datetime
import requests
import database
import pandas as pd
import numpy as np
from playwright.sync_api import Playwright, sync_playwright

total_result = dict()
now = datetime.datetime.now()
min = now.minute//10*10
index = now.replace(minute=min)
index1 = index.strftime("%Y-%m-%d %H:%M")
index2 = (index + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M")
index3 = (index + datetime.timedelta(minutes=-20)).strftime("%Y-%m-%d %H:%M")
total_df = pd.DataFrame(columns=['rf_10184100', 'rf_10184110', 'rf_10184140', 'swl', 'inf', 'sfw', 'ecpc', 'tototf', 'tide_level', 'fw_1018662', 'fw_1018683', 'fw_1019630', 'wl_1018662', 'wl_1018680', 'wl_1018683', 'wl_1019630'], index=[index1, index2, index3])
total_df.index.name = 'ymdhm'

# tide_level
def 강화대교_조위_sub_request():
    URL = f'https://www.khoa.go.kr/api/oceangrid/tideObs/search.do?ServiceKey=kH9DXri8W9Ny6w0onLeuqw==&ObsCode=DT_0032&Date={now.strftime("%Y%m%d")}&ResultType=json'
    request_headers = { 
    'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
    Safari/537.36'), } 
    response = requests.get(URL, headers = request_headers)
    return response.json()
def 강화대교_조위():
    # -1을 하는 경우 각기 다른 시간대의 자료가 수집될 수 있다.
    # 바로 20분이 되었다고 가정했을 때, 그 시각에 강화대교의 조위는 업데이트 되었을지 모르지만,
    # 청담대교의 수위는 업데이트가 안되었을지 모른다.
    # 다른 시간대의 자료를 모아 추정하는 것 보다는 차라리 10분 전의 같은 시각의 자료를 모으는게 나을듯
    강화대교_조위_result = 강화대교_조위_sub_request()
    try:
        temp_data = 강화대교_조위_result['result']['data'][-3]['record_time']
    except:
        temp_data = 강화대교_조위_result['result']['data'][-6]['record_time']
    curdate = datetime.datetime.strptime(temp_data, '%Y-%m-%d %H:%M:%S')
    change_date = curdate.replace(minute=curdate.minute//10*10)
    강화대교_조위_result['result']['data'].reverse()
    for i in range(20):
        if 강화대교_조위_result['result']['data'][i]['record_time'] == change_date.strftime('%Y-%m-%d %H:%M:%S'):
            # print(강화대교_조위_result['result']['data'][i])
            # {'tide_level': '99', 'record_time': '2022-08-24 23:50:00'}
            output_date = 강화대교_조위_result['result']['data'][i]['record_time'][:-3]
            output_tide_level = 강화대교_조위_result['result']['data'][i]['tide_level']
            output = (output_date, output_tide_level)
            return output
# print(강화대교_조위())
# ('2022-08-25 11:00', '174')
result = 강화대교_조위()
total_df.loc[result[0], 'tide_level'] = int(result[1].replace(',','').replace('-','0'))
# print(total_df)


# 팔당댐 저수량, 공용량
def 팔당댐_저수량_공용량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/sumun/damList.do')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    output_date = page.query_selector('#ymdhm').get_attribute('value')
    content2 = page.locator('#contents > table > tbody > tr:nth-child(11)')
    temp = content2.locator('td').all_text_contents()
    temp = [i.strip() for i in temp][2:4]
    저수량 = temp[0]
    공용량 = temp[1]
    output = (output_date, 저수량, 공용량)
    return output
with sync_playwright() as playwright:
    result = 팔당댐_저수량_공용량(playwright)
# print(result)
# ('2022-08-25 11:20', '211.410', '32.590')
total_df.loc[result[0], 'sfw'] = float(result[1].replace(',','').replace('-','0'))
total_df.loc[result[0], 'ecpc'] = float(result[2].replace(',','').replace('-','0'))
# print(total_df)


# 팔당댐 현재수위, 유입량, 총방류량
def 팔당댐_수위_유입량_방류량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/damPopup.do?Obscd=1017310')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:6]
    one = data[:3]
    one.insert(0, date[0])
    two = data[3:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 팔당댐_수위_유입량_방류량(playwright)
# print(result)
# [['2022-08-25 11:30', '25.000', '970.960', '970.960'], ['2022-08-25 11:20', '25.000', '961.400', '961.400']]
for i in result:
    total_df.loc[i[0], 'swl'] = float(i[1].replace(',','').replace('-','0'))
    total_df.loc[i[0], 'inf'] = float(i[2].replace(',','').replace('-','0'))
    total_df.loc[i[0], 'tototf'] = float(i[3].replace(',','').replace('-','0'))
# print(total_df)


# 청담대교 수위, 유량
def 청담대교_수위_유량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018662')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:6]
    one = data[:3]
    one.insert(0, date[0])
    two = data[3:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 청담대교_수위_유량(playwright)
# print(result)
# [['2022-08-25 12:40', '1.83', '865.81', '3.58'], ['2022-08-25 12:30', '1.85', '885.45', '3.60']]
for i in result:
    total_df.loc[i[0], 'wl_1018662'] = float(i[3].replace(',','').replace('-','0'))*100
    total_df.loc[i[0], 'fw_1018662'] = float(i[2].replace(',','').replace('-','0'))
# print(total_df)


# 잠수교 수위
def 잠수교_수위(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018680')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:6]
    one = data[:3]
    one.insert(0, date[0])
    two = data[3:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 잠수교_수위(playwright)
# print(result)
# [['2022-08-25 12:40', '3.49', '-', '3.42'], ['2022-08-25 12:30', '3.50', '-', '3.43']]
for i in result:
    total_df.loc[i[0], 'wl_1018680'] = float(i[3].replace(',','').replace('-','0'))*100
# print(total_df)


# 한강대교 수위, 유량
def 한강대교_수위_유량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018683')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:6]
    one = data[:3]
    one.insert(0, date[0])
    two = data[3:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 한강대교_수위_유량(playwright)
# print(result)
# [['2022-08-25 13:30', '1.27', '-', '3.34'], ['2022-08-25 13:20', '1.29', '1,211.25', '3.36']]
for i in result:
    total_df.loc[i[0], 'wl_1018683'] = float(i[3].replace(',','').replace('-','0'))*100
    total_df.loc[i[0], 'fw_1018683'] = float(i[2].replace(',','').replace('-','0')) # - 처리
# print(total_df)


# 행주대교 수위, 유량
def 행주대교_수위_유량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1019630')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:6]
    one = data[:3]
    one.insert(0, date[0])
    two = data[3:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 행주대교_수위_유량(playwright)
# print(result)
# [['2022-08-25 13:50', '2.39', '1,195.22', '3.19'], ['2022-08-25 13:40', '2.40', '1,213.16', '3.20']]
for i in result:
    total_df.loc[i[0], 'wl_1019630'] = float(i[3].replace(',','').replace('-','0'))*100
    total_df.loc[i[0], 'fw_1019630'] = float(i[2].replace(',','').replace('-','0')) # - 처리
# print(total_df)


# 대곡교 강수량
def 대곡교_강수량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184100')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:4]
    one = data[:2]
    one.insert(0, date[0])
    two = data[2:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 대곡교_강수량(playwright)
# print(result)
# [['2022-08-25 14:00', '0.0', '2.0'], ['2022-08-25 13:50', '0.0', '2.0']]
for i in result:
    total_df.loc[i[0], 'rf_10184100'] = float(i[1].replace(',','').replace('-','0'))
# print(total_df)


# 진관교 강수량
def 진관교_강수량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184110')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:4]
    one = data[:2]
    one.insert(0, date[0])
    two = data[2:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 진관교_강수량(playwright)
# print(result)
# [['2022-08-25 14:10', '0.0', '1.0'], ['2022-08-25 14:00', '0.0', '1.0']]
for i in result:
    total_df.loc[i[0], 'rf_10184110'] = float(i[1].replace(',','').replace('-','0'))
# print(total_df)


# 송정동 강수량
def 송정동_강수량(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto('http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184140')
    time.sleep(5)
    page.wait_for_load_state(timeout=3)
    content = page.locator('body > div.contents > div.table > table.scroll > tbody')
    date = content.locator('th').all_text_contents()[:2]
    data = content.locator('td').all_text_contents()[:4]
    one = data[:2]
    one.insert(0, date[0])
    two = data[2:]
    two.insert(0, date[-1])
    output = [(one), (two)]
    return output
with sync_playwright() as playwright:
    result = 송정동_강수량(playwright)
# print(result)
# [['2022-08-25 14:10', '0.0', '2.0'], ['2022-08-25 14:00', '0.0', '2.0']]
for i in result:
    total_df.loc[i[0], 'rf_10184140'] = float(i[1].replace(',','').replace('-','0'))

na_num = {}
for i in range(len(total_df)):
    na_num[f"{str(i)}"] = total_df.iloc[i,:].isna().sum()
# print(na_num["1"]) # {0: 16, 1: 0, 2: 3}
total_df = total_df.fillna(method='ffill')
total_df = total_df.fillna(method='bfill')
save_list = total_df.iloc[1,:].tolist()
save_list.insert(0, total_df.index.values[1])
save_list = tuple(map(str, save_list))
temp_col = list(total_df.columns)
temp_col.insert(0, 'ymdhm')
temp_col = tuple(temp_col)

db = database.SqliteDb()
db.connect('/root/web/water.db')
# db.connect('./water.db')
if not db.exists_table('water_total'):
    db.make_table('water_total')
    db.add_column('water_total', 'ymdhm')
    db.add_column('water_total', 'rf_10184100')
    db.add_column('water_total', 'rf_10184110')
    db.add_column('water_total', 'rf_10184140')
    db.add_column('water_total', 'swl')
    db.add_column('water_total', 'inf')
    db.add_column('water_total', 'sfw')
    db.add_column('water_total', 'ecpc')
    db.add_column('water_total', 'tototf')
    db.add_column('water_total', 'tide_level')
    db.add_column('water_total', 'fw_1018662')
    db.add_column('water_total', 'fw_1018683')
    db.add_column('water_total', 'fw_1019630')
    db.add_column('water_total', 'wl_1018662')
    db.add_column('water_total', 'wl_1018680')
    db.add_column('water_total', 'wl_1018683')
    db.add_column('water_total', 'wl_1019630')
    db.comm()
db.insert_data_with_cols('water_total', temp_col, save_list)
db.comm()
# ('2022-08-27 23:00', '0.0', '0.0', '0.0', '25.05', '565.31', '213.23', '30.77', '565.31', '207.0', '673.2', '0.0', '1249.45', '337.0', '330.0', '332.0', '322.0')
# print(save_list)

water_db = db.get_dataframe('water_total')
water_db.drop('idx', axis=1, inplace=True)
water_db.drop_duplicates(inplace=True)
water_db = water_db.astype(({'inf': 'float', 'fw_1018683': 'float'}))
water_db.drop_duplicates(['ymdhm'], keep = 'last', inplace=True)
water_db['inf'].replace(0.0, np.NaN, inplace=True)
water_db['fw_1018683'].replace(0.0, np.NaN, inplace=True)
water_db['inf'].interpolate(inplace=True)
water_db['fw_1018683'].interpolate(inplace=True)

if db.exists_table('water_collection'):
    db.drop_table('water_collection')
    db.comm()

db.to_sql('water_collection', water_db)
db.close()


