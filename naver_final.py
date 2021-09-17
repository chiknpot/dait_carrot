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



#stroe basic info
def scrap(store_ID,s_name,data,page):
    driver = webdriver.Chrome('./chromedriver')

    # wait until page loading
    driver.implicitly_wait(3)
    driver.get(page)
    driver.implicitly_wait(2)

    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    try:
        btn = '#_pcmap_list_scroll_container > ul > li > div:nth-child(1) > a'
        mainpageBtn=driver.find_elements_by_css_selector(btn)[0]
        mainpageBtn.click()
        time.sleep(8)
    except:
        print("no need to move mainpage")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # mArticle > div:nth-child(7) > div.particular_head
    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))

    time.sleep(4)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))

    #################### store - basic info ##################
    # five-star rating data
    try:
        s_rating = soup.select('#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span._1Y6hi._1A8_M > em')[0].text
        print("s_rating: " + s_rating)
    except:
        print("no s_rating")
        s_rating = ""

    # visit review count data
    try:
        v_count = soup.select("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span:nth-child(2) > a > em")[0].text.replace(',','')
        print("v_count: " + v_count)
    except:
        v_count = ""
        print("no v_count")

    # blog review count data
    try:
        s_blog = soup.select("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR._2z4r0 > div > span:nth-child(3) > a > em")[0].text.replace(',','')
        print("s_blog: " + s_blog)
    except:
        s_blog = ""
        print("no s_blog")

    data.append([store_ID, str(s_name), v_count, s_rating, s_blog])



    driver.close()
    driver.quit()





#store review info
def scrap2(store_ID, data,page):
    driver = webdriver.Chrome('./chromedriver')

    # wait until page loading
    driver.implicitly_wait(3)

    # scraping address insert
    driver.get(page)
    driver.implicitly_wait(4)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))
    time.sleep(2)


    try:
        btn = '#_pcmap_list_scroll_container > ul > li > div:nth-child(1) > a'
        mainpageBtn=driver.find_elements_by_css_selector(btn)[0]
        mainpageBtn.click()
        time.sleep(5)
    except:
        print("no need to move mainpage")


    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))

    time.sleep(4)


    #page source for main page click
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    driver.execute_script("window.scrollTo(0, 4000)")
    time.sleep(1)

    # declare / page source for review btn
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        btn = '#app-root > div > div > div.place_detail_wrapper > div:nth-child(5) > div > div.place_section._2Sq-S > div._2kAri > a'
        reviewBtn=driver.find_elements_by_css_selector(btn)[0]
        reviewBtn.click()
        time.sleep(1)
    except:
        print("no need to spread unfold review")

    # scroll down to loading
    driver.execute_script("window.scrollTo(0, 1500)")
    time.sleep(2)

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
            rating = record.select('div._1ZcDn > div._3D_HC > span._2tObC')[0].text
        except:
            rating=""

        try:
            review = str(record.select('div.PVBo8 > a > span')[0].text.strip('\n'))
        except:
            review = ""

        try:
            date = record.select('div._1ZcDn > div.ZvQ8X > span:nth-child(1)')[0].text
        except:
            date = ""

        try:
            u_vcount1 = record.select('div._1ZcDn > div.ZvQ8X > span:nth-child(2)')[0].text
            u_vcount = u_vcount1[:1]
        except:
            u_vcount = ""


        try:
            u_rcount1 = record.select('div._23Rml > a > div > div.ql4ZC > span:nth-child(1)')[0].text.replace(',','')
            title = u_rcount1.split(' ')[0]

            if str(title) == "리뷰":
                u_rcount = u_rcount1.split(' ')[1]
                #print(u_rcount)

            elif title[:2] == "평균":
                u_rcount = ""
                u_avg = str(title)[4:]
                data.append([store_ID, date, rating, review, u_rcount, u_vcount, u_avg])
                # user id setting

                continue

            else:
                u_rcount = ""
                u_avg = ""
                data.append([store_ID, date, rating, review, u_rcount, u_vcount, u_avg])
                # user id setting

                continue
        except:
            u_rcount = ""


        try:
            u_avg = record.select('div._23Rml > a > div > div.ql4ZC > span:nth-child(2)')[0].text
            title = u_avg.split(' ')[0]
            if str(title)[:2] == "평균":
                u_avg = str(title)[4:]
                #print(u_avg)
                data.append([store_ID, date, rating, review, u_rcount, u_vcount, u_avg])
                # user id setting

                continue
            else:
                u_avg = ""
        except:
            u_avg = ""



        try:
            u_avg = record.select('div._23Rml > a > div > div.ql4ZC > span:nth-child(3)')[0].text
            title = u_avg.split(' ')[0]
            if str(title)[:2] == "평균":
                u_avg = str(title)[4:]
                print(u_avg)
            else:
                u_avg = ""
        except:
            u_avg = ""


        data.append([store_ID, date, rating, review, u_rcount, u_vcount, u_avg])



        #print(data)

    driver.close()
    driver.quit()





store = ["베라 한남","한남족발"]


#_pcmap_list_scroll_container > ul > li:nth-child(1) > div._3ZU00._1rBq3 > a:nth-child(1) > div > div > span._3Apve
basic_info = []
review_info = []

store_ID = 1
for i in store:
    address = "https://map.naver.com/v5/search/한남동" + i + "?c=14137387.2230702,4514264.5328215,15,0,0,0,dh"
    scrap(store_ID,str(i),basic_info,address)
    #scrap2(store_ID, review_info, address)
    print(basic_info)
    #print(review_info)

    store_ID += 1



df1 = pd.DataFrame(basic_info, columns=['store_ID','s_name', 'v_count','s_rating', 's_blog'])
df2 = pd.DataFrame(review_info, columns=['store_ID', 'date', 'rating', 'review', 'u_rcount', 'u_vcount', 'u_avg'])

df1.to_csv('./n_store_info.csv', sep=',', na_rep='NaN',index = False,encoding='utf-8-sig')
df2.to_csv('./n_review_info.csv', sep=',', na_rep='NaN',index = False,encoding='utf-8-sig')

