# 크롤링한 데이터를 API로 제공하는 서버 코드
# 크롤링 시간을 단축하기 위해 멀티스레드로 크롤링을 진행합니다.
# 크롤링한 데이터를 JSON 형태로 반환합니다.
# 인터파크, 네이버, 카약 사이트에서 데이터를 크롤링합니다.

from flask import Flask, jsonify, render_template, request
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
from interpark import scrap_interpark
from naver import scrap_naver
from kayak import scrap_kayak
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

@app.route('/api/data/<start>/<dest>')
def get_data(start, dest):
    date = request.args.get('date', (datetime.datetime.now() + datetime.timedelta(days=1)))

    with ThreadPoolExecutor() as executor:
        future_interpark = executor.submit(scrap_interpark, start, dest, date)
        future_naver = executor.submit(scrap_naver, start, dest, date)
        future_kayak = executor.submit(scrap_kayak, start, dest, date)

    data_interpark = future_interpark.result()
    data_naver = future_naver.result()
    data_kayak = future_kayak.result()

    return jsonify({
        'interpark': data_interpark,
        'naver': data_naver,
        'kayak': data_kayak
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
