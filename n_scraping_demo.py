from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display
import time
import openpyxl
import csv
from IPython.display import display


#basic info
def scrap(data,page):
    driver = webdriver.Chrome('./chromedriver')

    # wait until page loading
    driver.implicitly_wait(3)


    # scraping address insert
    driver.get(page)
    driver.implicitly_wait(4)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))

    time.sleep(2)

    #declare / page source insert to 'soup'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)


#################### store - basic info ##################
    # five-star rating data
    try:
        star_rating = soup.select('#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span._1Y6hi._1A8_M > em')[0].text
        print("point: " + star_rating)
    except:
        print("no star_rating")

    # visit review count data
    try:
        visit_count = soup.select("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span:nth-child(2) > a > em")[0].text
        print("visit_count: " + visit_count)
    except:
        print("no visit_count")

    # blog review count data
    try:
        blog_count = soup.select("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span:nth-child(3) > a > em")[0].text
        print("blog_count: " + blog_count)
    except:
        print("no blog_count")

    data.append([star_rating, visit_count, blog_count])


    driver.close()
    driver.quit()




#detail review info
def scrap2(data,page):
    driver = webdriver.Chrome('./chromedriver')

    # wait until page loading
    driver.implicitly_wait(3)

    # scraping address insert
    driver.get(page)
    driver.implicitly_wait(4)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))
    time.sleep(1)

    #driver.execute_script("window.scrollTo(0, 1500)")
    #time.sleep(2)


    # declare / page source insert to 'soup'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    btn = '#app-root > div > div > div.place_detail_wrapper > div.place_fixed_maintab > div > div > div > div > a:nth-child(3)'
    reviewBtn=driver.find_elements_by_css_selector(btn)[0]
    reviewBtn.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, 1500)")
    time.sleep(1)

#################### store - review detail info ##################

    # next page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    while True:
        btn = '#app-root > div > div > div.place_detail_wrapper > div:nth-child(5) > div:nth-child(4) > div:nth-child(5) > div._2kAri > a'
        try:
            nextBtn=driver.find_elements_by_css_selector(btn)[0]
            nextBtn.click()
            time.sleep(1)
        except:
            print("nextBtn finished")
            time.sleep(1)
            break

    #scratping data reload
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    box = soup.select('#app-root > div > div > div.place_detail_wrapper > div:nth-child(5) > div:nth-child(4) > div:nth-child(5) > div > ul > li')



    #scraping review data
    for record in box:
        try:
            star_rating = record.select('div._1ZcDn > div._3D_HC > span._2tObC')[0].text
        except:
            star_rating=""

        try:
            review = record.select('div.PVBo8 > a > span')[0].text.strip('\n')
        except:
            review = ""

        try:
            date = record.select('div._1ZcDn > div.ZvQ8X > span:nth-child(1)')[0].text
        except:
            date = ""

        try:
            visit = record.select('div._1ZcDn > div.ZvQ8X > span:nth-child(2)')[0].text
        except:
            visit = ""

        try:
            receipt = record.select('div._1ZcDn > div.ZvQ8X > span:nth-child(3)')[0].text
        except:
            receipt = ""


        data.append([star_rating, review, date, visit, receipt])



    driver.close()
    driver.quit()



###############  main ###################
basic_info = []
review_info = []


#입력해야하는
store = '그랜드하얏트서울_스테이크하우스'
address = "https://map.naver.com/v5/search/%EA%B7%B8%EB%9E%9C%EB%93%9C%ED%95%98%EC%96%8F%ED%8A%B8%20%EC%84%9C%EC%9A%B8%20%EC%8A%A4%ED%85%8C%EC%9D%B4%ED%81%AC%ED%95%98%EC%9A%B0%EC%8A%A4%20/place/38576344?c=14136920.2378063,4514264.5328215,15,0,0,0,dh"
scrap(basic_info,address)
scrap2(review_info, address)


print(basic_info)
print(review_info)

#result data file
df1 = pd.DataFrame(basic_info, columns=['point', 'visit_count', 'blog_count'])
df2 = pd.DataFrame(review_info, columns=['point', 'review', 'date', 'visit','receipt'])

df1.to_excel('./basic_'+str(store)+'.xlsx', index=False)
df2.to_excel('./review_'+str(store)+'.xlsx', index=False)




