# pip install playwright
# playwright codegen url
from re import T
from playwright.sync_api import Playwright, sync_playwright
import datetime
import time

# 한강홍수통제소
# 대곡교, 진관교, 송정동
# 2012-05-01 00:00 ~ 2012-10-31 23:50
# ...
# 2022-05-01 00:00 ~ 2022-07-18 23:50
# http://www.hrfco.go.kr
# 에서 크롤링을 하는데 최대 14일 데이터만 한번에 가져올 수 있다.
# 가져올 데이터 형식
# 시간, 강수량, 누적강수량
# 원하는 데이터 형식
# 시간, 강수량

대곡교_url = "http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184100&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EB%8C%80%EA%B3%A1%EA%B5%90)&Edt=2022-08-08%2010:30"
진관교_url = "http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184110&Obsnm=%EB%82%A8%EC%96%91%EC%A3%BC%EC%8B%9C(%EC%A7%84%EA%B4%80%EA%B5%90)&Edt=2022-08-08%2018:50"
송정동_url = "http://www.hrfco.go.kr/popup/rainfallPopup.do?Obscd=10184100&Obsnm=%EC%84%9C%EC%9A%B8%EC%8B%9C(%EB%8C%80%EA%B3%A1%EA%B5%90)&Edt=2022-08-08%2010:30"
download_url = ""

def run(playwright: Playwright, start_date="20120501") -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    )
    page = context.new_page()
    page.goto(송정동_url)

    while(int(start_date) < 20220801):
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
            download.save_as(f"{ss.year}-{ss.month:02d}-{ss.day:02d}.xls")
        except:
            pass
        ee = ee + datetime.timedelta(days=1)
        start_date=f"{ee.year}{ee.month:02d}{ee.day:02d}"

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
