import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


options = webdriver.ChromeOptions()
# 창 안 뜨게하기
options.add_argument('headless')
chromedriver_path = "chromedriver"
# chromedriver 열기
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)


def main():
    # 렌더링 될때까지 4초 기다리기
    driver.implicitly_wait(4)
    # 주소 가져오기
    driver.get('https://map.kakao.com/')

    # 검색할 목록
    place_infos = ['다운타우너 한남', '오아시스 한남점', '리틀넥 한남', '빠레뜨한남 한남', '소브스한남', '베라 한남점', '루트에브리데이한남점',
                       '언더야드', '그랜드하얏트서울 스테이크하우스','아노브 한남']
    # 저장할 빈 리스트 선언
    all_r = []

    for i, place in enumerate(place_infos):
        # delay
        if i % 4 == 0 and i != 0:
            sleep(5)
        print("#####", i)
        search(place,all_r)

    driver.quit()
    print("finish")


def search(place,all_r):
    # 주소 가져오기
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
    # 검색어 입력
    search_area.send_keys(place)
    # Enter로 검색
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
    sleep(1)

    # 검색된 정보가 있는 경우에만 탐색
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    crawling(place,all_r)
    search_area.clear()



def crawling(place,all_r):
    """
    페이지 목록을 받아서 크롤링 하는 함수
    :param place: 리뷰 정보 찾을 장소이름
    """

    while_flag = False

    detail_page_xpath = '//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]'
    driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
    # 상세정보 탭으로 변환
    driver.switch_to.window(driver.window_handles[-1])
    sleep(1)

    # 첫 페이지
    extract_review(all_r)

    # 2-5 페이지
    idx = 3
    try:
        page_num = len(driver.find_elements_by_class_name('link_page'))  # 페이지 수 찾기
        for i in range(page_num - 1):
            # css selector를 이용해 페이지 버튼 누르기
            driver.find_element_by_css_selector(
                '#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(
                    idx) + ')').send_keys(Keys.ENTER)
            sleep(1)
            extract_review(all_r)
            idx += 1
        driver.find_element_by_link_text('다음').send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
        sleep(1)
        extract_review(all_r)  # 리뷰 추출
    except (NoSuchElementException, ElementNotInteractableException):
        print("no review in crawling")

    # 그 이후 페이지
    while True:
        idx = 4
        try:
            page_num = len(driver.find_elements_by_class_name('link_page'))
            for i in range(page_num - 1):
                driver.find_element_by_css_selector(
                    '#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(
                        idx) + ')').send_keys(Keys.ENTER)
                sleep(1)
                extract_review(all_r)
                idx += 1
            driver.find_element_by_link_text('다음').send_keys(Keys.ENTER)  # 10페이지 이상으로 넘어가기 위한 다음 버튼 클릭
            sleep(1)
            extract_review(all_r)  # 리뷰 추출
        except (NoSuchElementException, ElementNotInteractableException):
            print("no review in crawling")
            break

    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환


def extract_review(all_r):

    ret = True

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    place_name = soup.select('div.place_details > div > h2')[0].text

    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')

    # 리뷰가 있는 경우
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.txt_comment > span')  # 리뷰
            rating = review.select('.grade_star > em')  # 별점
            date = review.select("div.comment_info > div > span.time_write")  # 날짜
            val = ''
            if len(comment) != 0:
                if len(rating) != 0:
                    comment = comment[0].text
                    rating = rating[0].text.replace('점', '')
                    date = date[0].text
                else:
                    comment = comment[0].text
                    rating = 0
                    date = date[0].text

                all_r.append([place_name, date, rating,comment])

    else:
        print('no review in extract')
        ret = False

    df = pd.DataFrame(all_r, columns=["이름","date","rating","review"])
    df.to_csv('./k_scraping_demo.csv', index=False, encoding='utf-8-sig')
    df.to_excel('./k_scraping_demo.xlsx', index=False, encoding='utf-8-sig')
    return ret


if __name__ == "__main__":
    main()
