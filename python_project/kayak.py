# 카약 항공사 크롤링
# 출발지, 도착지, 날짜를 입력받아 해당 날짜의 최저가와 최고가를 반환
# 최고가, 최저가, url을 반환

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import concurrent.futures
import time


def scrap_kayak(start, dest, date):
    try:
        lowest_price_url = f"https://www.kayak.co.kr/flights/{start}-{dest}/{date}?sort=price_a"
        highest_price_url = f"https://www.kayak.co.kr/flights/{start}-{dest}/{date}?sort=price_b"

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
        
        driver.get(lowest_price_url)
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        lowest_price_element = soup.select_one("#listWrapper > div > div:nth-child(2) > div > div:nth-child(2) > div.yuAt.yuAt-pres-rounded > div > div > div.nrc6-price-section > div > div.Oihj-bottom-booking > div > div.M_JD-large-display > div.oVHK > a > div > div > div > div")
        lowest_price = lowest_price_element.text.strip() if lowest_price_element else None
        lowest_price = lowest_price.replace("원", "")

        driver.get(highest_price_url)
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        highest_price_element = soup.select_one("#listWrapper > div > div:nth-child(2) > div > div:nth-child(2) > div.yuAt.yuAt-pres-rounded > div > div > div.nrc6-price-section > div > div.Oihj-bottom-booking > div > div.M_JD-large-display > div.oVHK > a > div > div > div > div")
        highest_price = highest_price_element.text.strip() if highest_price_element else None
        highest_price = highest_price.replace("원", "")

        driver.quit()
        print(f"최저가: {lowest_price}, 최고가: {highest_price}")

        if lowest_price and highest_price:
            return {'kayak': {
                    'cheapest_price': lowest_price,
                    'max_price': highest_price,
                    'url': lowest_price_url,
                }
            }
        else:
            return {'error': 'Could not find the price elements'}

    except Exception as e:
        return {'error': f'An error occurred during scraping: {str(e)}'}