import requests
import re
import time
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# capa = DesiredCapabilities.CHROME
# capa["pageLoadStrategy"] = "none"


def getMushroomData(browser,key,*isAll):
    testkey = '朱辛庄'
    url = "http://bj.mgzf.com/list/?searchWord=" + testkey
    browser.get(url)
    # searchBox = browser.find_element_by_class_name('search-box')
    # input = searchBox.find_element_by_tag_name('input')
    # input.send_keys(key)
    # input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'small-container')))
    result = []
    resultTemp = getMushroomListData(browser)
    result.extend(resultTemp)
    if isAll:
        nextPageDiv = browser.find_element_by_class_name('page-box')
        nextNodeList = nextPageDiv.find_elements_by_css_selector('p>a')
        if len(nextNodeList) > 1:
            k = 1
            for k in range(len(nextNodeList) -1):
                # nextNode = nextPageDiv.find_element_by_xpath('//a[text()="下一页"]')
                nextPageDiv = browser.find_element_by_class_name('page-box')
                nextNodeList = nextPageDiv.find_elements_by_css_selector('p>a')
                nextNode = nextNodeList[k+1]
                print(nextNode.text,'nextNode.text')
                if nextNode:
                    nextNode.click()
                    wait = WebDriverWait(browser, 10)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'small-container')))
                    time.sleep(0.5)
                    resultTemp = getMushroomListData(browser)
                    result.extend(resultTemp)

    return result

def getMushroomListData(browser):
    roomListBox = browser.find_element_by_class_name('small-container')
    roomList = roomListBox.find_elements_by_tag_name('a')
    result = []
    for i in roomList:
        detailUrl = i.get_attribute('href')
        title = i.get_attribute('title')
        imgDiv = i.find_element_by_class_name('image-box')
        img = imgDiv.find_element_by_tag_name('img')
        imgSrc = img.get_attribute("src")
        middleDiv = i.find_element_by_class_name('text-content-middle')
        areaDiv = middleDiv.find_element_by_tag_name('h2').text
        area = areaDiv.split('-')[-1:][0]
        distance = middleDiv.find_element_by_tag_name('p').text
        tagDiv = middleDiv.find_element_by_class_name('iconList')
        tagDivList = tagDiv.find_elements_by_tag_name('img')
        tagList = []
        for k in tagDivList:
            tagList.append(k.get_attribute('title'))

        priceDiv = i.find_element_by_class_name('text-content-right')
        priceSpan = priceDiv.find_element_by_class_name('price')
        price = priceSpan.find_element_by_tag_name('span').text

        res = {
            "imgSrc":imgSrc,
            'title':title,
            'detailUrl':detailUrl,
            'area':area,
            'floor':0,
            'floorTotal':0,
            'distance':distance,
            'tagList':tagList,
            'price':price

        }
        result.append(res)
    
    return result
