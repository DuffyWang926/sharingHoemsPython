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
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# capa = DesiredCapabilities.CHROME
# capa["pageLoadStrategy"] = "none"

    
def getZiRoomData(browser, key, isAll):
    browser.get('http://www.ziroom.com')
    searchBox = browser.find_element_by_class_name('Z_search_main')
    input = searchBox.find_element_by_tag_name('input')
    input.send_keys(key)
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
    result = []
    resultTemp = getZiRoomListData(browser)
    result.extend(resultTemp)
    if isAll:
        nextPageDiv = browser.find_element_by_class_name('Z_pages')
        nextNodeList = nextPageDiv.find_elements_by_tag_name('a')
        if len(nextNodeList) > 2:
            for k in range(len(nextNodeList) -2):
                wait = WebDriverWait(browser, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
                if len(nextNodeList) > 2:
                    nextNode = browser.find_element_by_xpath('//a[text()="下一页"]')
                    if nextNode:
                        resultTemp = getZiRoomListData(browser)
                        result.extend(resultTemp)
                        nextNode.click()

    return result

def getZiRoomListData(browser):
    result = []
    roomlist = browser.find_element_by_class_name('Z_list-box')
    items = roomlist.find_elements_by_class_name('item')
    
    for i in items:
        divList = i.find_elements_by_tag_name('span')

        if len(divList) > 5:
            detail = i.find_element_by_class_name('pic-wrap')
            detailUrl = detail.get_attribute('href')
            if detailUrl.find('http') == -1:
                detailUrl.replace('//','http://')
            img = i.find_element_by_class_name('lazy')
            imgSrc = img.get_attribute('src')
            if imgSrc.find('http') == -1:
                imgSrc.replace('//','http://')
            
            # titleDiv = i.find_element_by_class_name('info-box')
            titleNode = i.find_element_by_css_selector('h5>a')
            title = titleNode.text
            description = i.find_element_by_class_name('desc')
            descriptions = description.find_element_by_tag_name('div')
            floorData = descriptions.text
            floorArr = floorData.split('|')
            if len(floorArr) > 0:
                area = floorArr[0]
                floorTotalData = floorArr[1]
                floor = floorTotalData.split('/')[0]
                floorTotal = floorTotalData.split('/')[1].replace('层','').strip()

            distanceNode = description.find_element_by_class_name('location')
            distance = distanceNode.text.strip()
            priceDiv = i.find_element_by_class_name('price')
            priceNodeList = priceDiv.find_elements_by_class_name('num')
            priceList = []
            for k in priceNodeList:
                priceList.append(k.get_attribute('style').replace('//','http://'))

            tagNodeDiv = i.find_element_by_class_name('tag')
            tagNodeSpan = tagNodeDiv.find_elements_by_tag_name('span')
            tagList = []
            for k in tagNodeSpan:
                tagList.append(k.text)
            
            res = { 
                'imgSrc':imgSrc,
                'title':title,
                'area':area,
                'floor':floor,
                'floorTotal':floorTotal,
                'distance':distance,
                'price':priceList,
                'tagList':tagList,
                'detailUrl':detailUrl
                
                }
            result.append(res)

    return result
