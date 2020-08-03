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


def getEggShellData(browser,key,*isAll):
    browser.get('https://www.danke.com')
    searchBox = browser.find_element_by_class_name('search-box')
    input = searchBox.find_element_by_tag_name('input')
    input.send_keys(key)
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'roomlist')))
    result = []
    resultTemp = getEggListData(browser)
    result.extend(resultTemp)
    if isAll:
        nextPageDiv = browser.find_element_by_class_name('page')
        nextNodeList = nextPageDiv.find_elements_by_tag_name('a')
        if len(nextNodeList) > 2:
            for k in range(len(nextNodeList) -2):
                if len(nextNodeList) > 1:
                    nextNode = browser.find_element_by_xpath('//a[text()=" > "]')
                    if nextNode:
                        nextNode.click()
                        resultTemp = getEggListData(browser)
                        result.extend(resultTemp)

    return result

def getEggListData(browser):
    roomListBox = browser.find_element_by_class_name('r_ls_box')
    roomList = roomListBox.find_elements_by_class_name('r_lbx')
    result = []
    for i in roomList:
        img = i.find_element_by_tag_name('img')
        imgSrc = img.get_attribute("src")
        titleDiv = i.find_element_by_class_name('r_lbx_cena')
        titleNode = titleDiv.find_element_by_tag_name('a')
        title = titleNode.text
        detailUrl = titleNode.get_attribute('href')
        detailContent = i.find_element_by_class_name('r_lbx_cenb').text
        detailConList = detailContent.split('|')
        area = 0
        floor = 0
        if len(detailConList) > 2:
            area = detailConList[0].strip()[-3:]
            floor = detailConList[1].strip()[:-1]
        
        distanceDiv = i.find_element_by_class_name('r_lbx_cena')
        distance = distanceDiv.find_element_by_class_name('r_lbx_cena').text
        tagDiv = i.find_element_by_class_name('r_lbx_cenc')
        tagDivList = tagDiv.find_elements_by_tag_name('span')
        tagList = []
        for k in tagDivList:
            tagList.append(k.text)

        priceDiv = i.find_element_by_class_name('r_lbx_moneya')
        price = i.find_element_by_class_name('ty_b').text

        res = {
            "imgSrc":imgSrc,
            'title':title,
            'detailUrl':detailUrl,
            'area':area,
            'floor':floor,
            'distance':distance,
            'tagList':tagList,
            'price':price

        }
        result.append(res)
    
    return result
