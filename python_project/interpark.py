# 인터파크 항공사 크롤링
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
import time


def scrap_interpark(start, dest, date):
    try:
        date_without_dash = date.replace("-", "")
        url = f"https://fly.interpark.com/booking/mainFlights.do?tripType=OW&sdate0={date_without_dash}&sdate1=&sdate2=&dep0={start}&dep1=&dep2=&arr0={dest}&arr1=&arr2=&adt=1&chd=0&inf=0&via=&comp=Y&val=&bizCd=#list"

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

        sort_button_xpath = '/html/body/div[1]/div/div[5]/div/div/div[1]/div[3]/div[2]/div[1]/ul/li[7]/span'
        try:
            sort_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sort_button_xpath))
            )
            time.sleep(3)
            sort_button.click()
            time.sleep(2)
        except Exception as e:
            driver.quit()
            return {'error': 'Failed to sort prices'}

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="schedule0List"]/li[1]/div[7]/span[2]/strong'))
            )
        except Exception as e:
            driver.quit()
            return {'error': 'Failed to load price data'}

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        cheap_price_element = soup.select_one('#schedule0List > li:nth-child(1) > div.t7.last.align-right > span.charge > strong')
        cheapest_price = cheap_price_element.text.strip() if cheap_price_element else None

        try:
            sort_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, sort_button_xpath))
            )
            time.sleep(3)
            sort_button.click()
            time.sleep(2)
        except Exception as e:
            driver.quit()
            return {'error': 'Failed to sort prices'}

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        max_price_element = soup.select_one('#schedule0List > li:nth-child(1) > div.t7.last.align-right > span.charge > strong')
        max_price = max_price_element.text.strip() if max_price_element else None
        driver.quit()

        print(f"최저가: {cheapest_price}, 최고가: {max_price}")
        if cheapest_price and max_price:
            return {'interpark' : {
                    'cheapest_price': cheapest_price,
                    'max_price': max_price,
                    'url': url
                }
            }
        else:
            return {'error': 'Could not find the price elements'}

    except Exception as e:
        return {'error': 'An error occurred during scraping'}