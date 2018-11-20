# -*- coding: utf-8 -*-
'''
multiprocessing crawler for jandan.net/ooxx

"pip install -r requirements.txt" and run it.

The line with notes is position you can control this script.

Have fun.

@author: B1u3Buf4
'''
import os
import re
import time
from multiprocessing import Process, Queue, Pool
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class checkload(object):
    def __init__(self,driver):
        self.driver = driver


    def __call__(self,driver):
        return driver.find_element_by_id('comments').get_attribute("innerHTML").find('sinaimg.cn') > -1


def crawlurl():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get(url = 'http://jandan.net/ooxx')
    time.sleep(1)
    pics = []
    urls = []
    order = 1
    try:
        page = driver.page_source
        counts = re.findall('current-comment-page">.*</s', page)[0]
        cou = re.findall('[0-9]{1,4}', counts)
        cou = int(cou[0])
        for i in range(1, cou + 1): #start-page to end-page
            order = i
            print(order, len(pics))
            url = 'http://jandan.net/ooxx/page-' + str(i) + '#comments'
            driver.get(url)
            WebDriverWait(driver, 5, 0.5).until(checkload(driver))
            page = driver.find_element_by_id('comments').get_attribute("innerHTML")
            pics.extend(re.findall('(src=".*?jpg|src=".*?gif|src=".*?png)', page))
        for j in pics:
            url = re.sub('cn/.*?/', 'cn/large/', j[5:])
            if 'jandan.net' in url:
                continue
            if url.find('http://') != 0:
                print('[-]', url)
                continue
            urls.append(url)
        return urls
    finally:
        print('[+]', order, len(urls))
        driver.quit()


def tinyreq(url):
    r = requests.get(url)
    name1 = re.findall('([a-zA-Z0-9]*?.jpg|[a-zA-Z0-9]*?.gif|[a-zA-Z0-9]*?.png)', url[-36:])
    print('Downloading', url)
    with open('./pics/' + name1[0], "wb") as code:
        try:
            code.write(r.content)
        except:
            pass


def getpic(imgs, processes = 5): #number of processes
    pool = Pool(processes)
    for img in imgs:
        pool.apply_async(tinyreq, (img, ))
    pool.close()
    pool.join()


if __name__ == "__main__":
    if not os.path.exists('./pics/'):
        os.mkdir('pics')
    start_time = time.time()
    pic = crawlurl()
    getpic(pic)
    print('[+] total:%s S' % (int(time.time() - start_time)))
