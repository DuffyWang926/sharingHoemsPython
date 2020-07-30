import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions


from getHtml.eggShell import getEggShellData
from getHtml.ziRoomSelenium import getZiRoomData
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# capa = DesiredCapabilities.CHROME

def getMyHomeData(browser, key, isAll):
    browser.get('https://bj.5i5j.com/zufang/w3/')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-inp')))
    inputNode = browser.find_element_by_class_name('search-inp')
    input = inputNode.find_element_by_id('zufangw3')
    input.send_keys(key)
    input.send_keys(Keys.ENTER)
    time.sleep(1)
    webdriver.Chrome().refresh
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pList')))
    result = []

    resultTemp = getMyHomeListData(browser)
    result.extend(resultTemp)
    # if isAll:
    #     nextPageDiv = browser.find_element_by_class_name('Z_pages')
    #     nextNodeList = nextPageDiv.find_elements_by_tag_name('a')
    #     if len(nextNodeList) > 2:
    #         for k in range(len(nextNodeList) -2):
    #             wait = WebDriverWait(browser, 10)
    #             wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
    #             if len(nextNodeList) > 2:
    #                 nextNode = browser.find_element_by_xpath('//a[text()="下一页"]')
    #                 if nextNode:
    #                     resultTemp = getZiRoomListData(browser)
    #                     result.extend(resultTemp)
    #                     nextNode.click()
    return result

def getMyHomeListData(browser):
    result = []
    roomlist = browser.find_element_by_class_name('pList')
    items = roomlist.find_elements_by_tag_name('li')
    for i in items:
        imgDiv = i.find_element_by_class_name('listImg')
        detail = imgDiv.find_element_by_tag_name('a')
        detailUrl = detail.get_attribute('href')
        if detailUrl.find('http') == -1:
            detailUrl.replace('//','http://')

        img = imgDiv.find_element_by_css_selector('a>img')
        imgSrc = img.get_attribute('src')
        if imgSrc.find('data') != -1:
            imgSrc = img.get_attribute('data-src')

        if imgSrc.find('http') == -1:
            imgSrc.replace('//','http://')
        contentDiv = i.find_element_by_class_name('listCon')
        titleNode = contentDiv.find_element_by_css_selector('h3>a')
        title = titleNode.text
        detailConDiv= contentDiv.find_element_by_class_name('listX')
        pList = detailConDiv.find_elements_by_tag_name('p')
        area = ''
        floor = ''
        floorTotal = ''
        distance = ''
        if len(pList) > 1:
            textList = pList[0].text.split('·')
            print(textList,'textList')
            if len(textList) > 3:
                area = textList[1].strip()[:2]
                floorData = textList[3].strip().split('/')
                if len(floorData) > 1:
                    floor = floorData[0]
                    floorTotal = floorData[1][:-1]
            distanceNodeList = pList[1].find_elements_by_tag_name('a')
            if len(distanceNodeList) > 1:
                distance = distanceNodeList[1].text
        priceNode = detailConDiv.find_element_by_class_name('jia')
        price = priceNode.find_element_by_tag_name('strong').text
        res = { 
            'imgSrc':imgSrc,
            'title':title,
            'area':area,
            'floor':floor,
            'floorTotal':floorTotal,
            'distance':distance,
            'price':price,
            'detailUrl':detailUrl
            
            }
        result.append(res)
    return result
