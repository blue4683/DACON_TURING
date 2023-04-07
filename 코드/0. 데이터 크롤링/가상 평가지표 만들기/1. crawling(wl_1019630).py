# pip install playwright
# playwright codegen url
from re import T
from playwright.sync_api import Playwright, sync_playwright
import datetime
import time

'''
# 평가 모듈을 만들기 위해 필요한 자료
2022-06-01 00:00 ~ 2022-07-18 23:50 의 (청담대교, 잠수교, 한강대교, 행주대교) 10분 단위 수위
크롤링을 하는데 최대 14일 데이터만 한번에 가져올 수 있다.

데이터를 구하는 곳 : http://www.hrfco.go.kr/sumun/waterlevelList.do

* 청담대교(wl_1018662) : http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018662&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%B2%AD%EB%8B%B4%EB%8C%80%EA%B5%90)
* 잠수교(wl_1018680) : http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018680&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%9E%A0%EC%88%98%EA%B5%90)
* 한강대교(wl_1018683) : http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018683&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%95%9C%EA%B0%95%EB%8C%80%EA%B5%90)
* 행주대교(wl_1019630) : http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1019630&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%96%89%EC%A3%BC%EB%8C%80%EA%B5%90)

# 평가 규칙
평가 산식: RMSE / R_Squared_Score
R_Squared_Score <= 0인 경우 999출력
각 다리의 예측된 수위에 대한 점수를 평균하여 리더보드에 표시

'''

# 청담대교, 잠수교, 한강대교, 행주대교
download_url_dict = {
    "wl_1018662":"http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018662&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%B2%AD%EB%8B%B4%EB%8C%80%EA%B5%90)",
    "wl_1018680":"http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018680&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EC%9E%A0%EC%88%98%EA%B5%90)",
    "wl_1018683":"http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1018683&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%95%9C%EA%B0%95%EB%8C%80%EA%B5%90)",
    "wl_1019630":"http://www.hrfco.go.kr/popup/waterlevelPopup.do?Obscd=1019630&Sdt=2022-08-09%2016:00&Edt=2022-08-09%2016:00&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%ED%96%89%EC%A3%BC%EB%8C%80%EA%B5%90)"
}

def run(playwright: Playwright, start_date="20220601") -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
    page = context.new_page()
    page.goto(download_url_dict["wl_1019630"])

    while(int(start_date) < 20220810):
        # fill #datestart
        time.sleep(5)
        page.locator("#datestart").click()
        time.sleep(1)
        page.locator("#datestart").press("Control+a")
        time.sleep(1)
        ss = datetime.datetime.strptime(start_date, "%Y%m%d")
        temp_time = f"{ss.year}-{ss.month:02d}-{ss.day:02d} {ss.hour:02d}:{ss.minute:02d}"
        for i in temp_time:
            page.locator("#datestart").press(i)
        page.locator("text=닫기").click()

        # fill #dateend
        time.sleep(1)
        page.locator("#dateend").click()
        time.sleep(1)
        page.locator("#dateend").press("Control+a")
        time.sleep(1)
        ee = ss + datetime.timedelta(days=13)
        # for i in f"{ee.year}-{ee.month:02d}-{ee.day:02d} {ee.hour:02d}:{ee.minute:02d}":
        for i in f"{ee.year}-{ee.month:02d}-{ee.day:02d} 23:50":
            page.locator("#dateend").press(i)
        page.locator("text=닫기").click()
        time.sleep(1)

        page.locator("button:has-text(\"검색\")").click()
        time.sleep(5)
        try:
            with page.expect_download() as download_info:
                page.locator("button:has-text(\"저장\")").click()

            download = download_info.value
            download.save_as(f"wl_1019630_{ss.year}-{ss.month:02d}-{ss.day:02d}.xls")
        except:
            pass
        ee = ee + datetime.timedelta(days=1)
        start_date=f"{ee.year}{ee.month:02d}{ee.day:02d}"

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
