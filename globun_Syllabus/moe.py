import time
from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

url = '' #開きたいページのURLをいれる
driver.get(url)
