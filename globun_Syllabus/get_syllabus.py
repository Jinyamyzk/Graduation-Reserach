import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
import chromedriver_binary
from bs4 import BeautifulSoup
import requests
import csv
from janome.tokenizer import Tokenizer

def add_sum_class(nendo):
    soup = BeautifulSoup(page_source, 'html.parser')
    #tr_tagを取得
    table = soup.select_one('table.normal')
    tbody = table.select_one('tbody')
    tr_tags = tbody.select('tr')
    i=0
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all('td')
        syllabus_url = "https://kym-syllabus.ofc.kobe-u.ac.jp/kobe_syllabus/{}/13/data/{}_{}.html"
        syllabus_res = requests.get(syllabus_url.format(nendo,nendo,td_tags[7].text.strip()))
        syllabus_soup = BeautifulSoup(syllabus_res.text, "html.parser")
        class_names = syllabus_soup.select('body > table:nth-of-type(2) > tr:nth-of-type(2) > td > table > tr:nth-of-type(3) > td:nth-of-type(2)')
        codes = syllabus_soup.select('body > table:nth-of-type(2) > tr:nth-of-type(2) > td > table >  tr:nth-of-type(2) > td:nth-of-type(2)')
        quaters = syllabus_soup.select('body > table:nth-of-type(2) > tr:nth-of-type(2) > td > table > tr:nth-of-type(2) > td:nth-of-type(4)')
        themes = syllabus_soup.select('.gaibu-syllabus')

        strip_syllabus = []
        important_list = []
        for name in class_names:
            important_list.append(name.text.strip())
        important_list.append(nendo)
        for quater in quaters:
            important_list.append(quater.text.strip())
        for code in codes:
            important_list.append(code.text.strip())
        for theme in themes:
            strip_syllabus.append(theme.text.strip())
        important_list.append(strip_syllabus[0]) #授業のテーマ
        # important_list.append(strip_syllabus[3])
        # important_list.append(strip_syllabus[4])
        sum_class_info.append(important_list)
        time.sleep(1)
        i+=1
        # if i >= 1:
        #     break
        print(i)

#ウェブドライバーを起動
driver = webdriver.Chrome()

#最初の画面
url = 'https://kym-syllabus.ofc.kobe-u.ac.jp/campussy/campussquare.do?_flowExecutionKey=_c35C8A384-F668-2E5A-45B6-70E95EEE7501_k0AE26F4C-E58E-D295-B242-496080162875'
driver.get(url)
time.sleep(1)

#国際人間科学部を選択
#学部ボタンを押す
element = driver.find_element_by_css_selector("#menu > li:nth-child(1)")
element.click()
#移動
element = driver.find_element_by_css_selector("#menu > li.sub.click > ul > li:nth-child(4) > a")
element.click()
time.sleep(1)

sum_class_info = []

#年度(2017年)を選択
nendo = 2017
element = driver.find_element_by_css_selector("#nendo")
indexNum = 6
select = Select(element)
#セレクトタグのオプションをインデックス番号から選択する
select.select_by_index(indexNum)
time.sleep(1)

#月曜日
page_source=driver.page_source
add_sum_class(nendo)

#火曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#水曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(2)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#木曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(3)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#金曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(4)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#年度(2018年)を選択
nendo = 2018
element = driver.find_element_by_css_selector("#nendo")
indexNum = 7
select = Select(element)
#セレクトタグのオプションをインデックス番号から選択する
select.select_by_index(indexNum)
time.sleep(1)

#月曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#火曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#水曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(2)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#木曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(3)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#金曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(4)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#年度(2019年)を選択
nendo = 2019
element = driver.find_element_by_css_selector("#nendo")
indexNum = 8
select = Select(element)
#セレクトタグのオプションをインデックス番号から選択する
select.select_by_index(indexNum)
time.sleep(1)

#月曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#火曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#水曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(2)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#木曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(3)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#金曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(4)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#年度(2020年)を選択
nendo = 2020
element = driver.find_element_by_css_selector("#nendo")
indexNum = 9
select = Select(element)
#セレクトタグのオプションをインデックス番号から選択する
select.select_by_index(indexNum)
time.sleep(1)

#月曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#火曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(1)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#水曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(2)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#木曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(3)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

#金曜日
element = driver.find_element_by_css_selector("#jikanwariKeywordForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr > td > a:nth-child(4)")
element.click()
time.sleep(1)
page_source=driver.page_source
add_sum_class(nendo)

print(sum_class_info)

with open('/Users/Jinya/Desktop/Syllabus/globun_Syllabus/syllabus_globun.csv', 'w',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(["科目名","年度",'クォーター',"時間割コード","テーマ"])
        writer.writerows(sum_class_info)

driver.quit()
