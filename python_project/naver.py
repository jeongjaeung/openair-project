# 네이버 항공사 크롤링
# 출발지, 도착지, 날짜를 입력받아 해당 날짜의 최저가와 최고가를 반환
# 최고가, 최저가, url을 반환

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

def scrap_naver(start, dest, date):
    try:
        date_without_dash = date.replace("-", "")
        url = f'https://flight.naver.com/flights/international/{start}-{dest}-{date_without_dash}?adult=1&fareType=Y'

        options = ChromeOptions()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        options.add_argument('user-agent=' + user_agent)
        options.add_argument("lang=ko_KR")
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

        service = ChromeService(executable_path=ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        time.sleep(8)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        price_element = soup.select_one('#container > div.international_content__Vpjrs > div > div.indivisual_IndividualList__jqCMi > div.indivisual_results__tT38g > div:nth-child(1) > div > div.item_ItemPriceList__pAvJJ > div > div > div > b > i')
        cheapest_price = price_element.text.strip() if price_element else None
        time.sleep(4)
        max_price_element = soup.select_one('#container > div.international_content__Vpjrs > div > div.indivisual_IndividualList__jqCMi > div.indivisual_results__tT38g > div:nth-last-child(1) > div > div.item_ItemPriceList__pAvJJ > div > div > div > b > i')
        max_price = max_price_element.text.strip() if max_price_element else None

        print(f"최저가: {cheapest_price}, 최고가: {max_price}")
        driver.quit()

        if cheapest_price and max_price:
            return {'naver': {
                    'cheapest_price': cheapest_price,
                    'max_price': max_price,
                    'url': url
                }
            }
        else:
            return {'error': 'Could not find the price elements'}

    except Exception as e:
        return {'error': f'An error occurred during scraping: {str(e)}'}