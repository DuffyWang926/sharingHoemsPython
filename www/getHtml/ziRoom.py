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

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# capa = DesiredCapabilities.CHROME
# capa["pageLoadStrategy"] = "none"
def getZiRoomHtml(key):
    keyword=urllib.parse.quote(key.encode('gb2312'))
    # url = 'http://www.ziroom.com/z/?qwd={key}' 
    httpUrl =  'http://www.ziroom.com/z/'
    url =  httpUrl + '?qwd=' +  keyword
    urlNext = 'http://www.ziroom.com/z/z0/?qwd=' + keyword 
    r = requests.get(url)
    
    # soup = BeautifulSoup('<p class="body strikeout" style="background-image: url(//static8.ziroom.com/phoenix/pc/images/price/new-list/f4c1f82540f8d287aa53492a44f5819b.png);background-position: -171.2px"></p>','html')
    # p = soup.p
    
    # return p


    soup = BeautifulSoup(r.text,'html')
    items = soup.findAll('div', {'class': 'item'})
    result = []
    for i in items:
        detail = i.find('a',{'class':'pic-wrap'})
        detailUrl = detail['href'].replace('//','http://')
        img = i.find('img', {'class': 'lazy'})
        imgSrc = img['src']
        imgSrcEnd = imgSrc.replace('//','http://')
        titleNode = i.select('h5>a')
        title = titleNode[0].text
        description = i.find('div',{'class':'desc'})
        descriptions = description.select('div')
        floorData = descriptions[0].text
        floorArr = floorData.split('|')
        if len(floorArr) > 0:
            area = floorArr[0]
            floorTotalData = floorArr[1]
            floor = floorTotalData.split('/')[0]
            floorTotal = floorTotalData.split('/')[1].replace('层','').strip()

        distanceNode = description.select('div',{'class':'location'})
        distance = distanceNode[1].string.replace('\n','').replace('\t','').replace(' ','')
        priceNodeList = i.select('span[class="num"]')
        priceList = []
        for k in priceNodeList:
            priceList.append(k['style'].replace('//','http://'))
        
        tagNodeDiv = i.select('div[class="tag"]')
        tagNodeSpan = tagNodeDiv[0].select('span')
        tagList = []
        for k in tagNodeSpan:
            tagList.append(k.text)

        res = { 
            'imgSrc':imgSrcEnd,
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

def getZiRoomHtmlSelenium(key):
    browser = webdriver.Chrome()
    result = []
    resultEgg = []
    resultZiRoom = []
    resultMyHome = []
    try:
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=option)
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
           'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

        # resultEgg = getEggShellData(browser, '朱辛庄', True)
        # resultZiRoom = getZiRoomData(browser, '朱辛庄', True)
        resultMyHome = getMyHomeData(browser, '朱辛庄', True)
        print(resultMyHome,'resultMyHome333333')
        

        # browser.get('http://www.ziroom.com')
        # input = browser.find_element_by_id('Z_search_input')
        # input.send_keys(key)
        # input.send_keys(Keys.ENTER)
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
        print(browser.current_url,'browser.current_url')
        # print(browser.get_cookies(),'browser.get_cookies()')
        # print(browser.page_source,'browser.page_source')
    finally:
        browser.close()
    
    result.extend(resultEgg)
    result.extend(resultZiRoom)
    result.extend(resultMyHome)


    return result
    

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

            



    print(result,'result1111111111')

    return result

def getEggListData(browser):
    roomListBox = browser.find_element_by_class_name('r_ls_box')
    roomList = roomListBox.find_elements_by_class_name('r_lbx')
    # print(roomList,'roomList111111111')
    result = []
    for i in roomList:
        img = i.find_element_by_tag_name('img')
        imgSrc = img.get_attribute("src")
        titleDiv = i.find_element_by_class_name('r_lbx_cena')
        titleNode = titleDiv.find_element_by_tag_name('a')
        title = titleNode.text
        detailUrl = titleNode.get_attribute('href')
        
        detailContent = i.find_element_by_class_name('r_lbx_cenb').text
         
        # print(detailContent,'detailContent11111111')

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
            print('next')
            for k in range(len(nextNodeList) -2):
                wait = WebDriverWait(browser, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
                if len(nextNodeList) > 2:
                    nextNode = browser.find_element_by_xpath('//a[text()="下一页"]')
                    if nextNode:
                        resultTemp = getZiRoomListData(browser)
                        result.extend(resultTemp)
                        nextNode.click()

    print(result,'resultZi22222222222')
    
    return result

def getZiRoomListData(browser):
    result = []
    roomlist = browser.find_element_by_class_name('Z_list-box')
    items = roomlist.find_elements_by_class_name('item')
    
    for i in items:
        divList = i.find_elements_by_tag_name('span')
        print(len(divList),'i.text**********')
        # print(i.text,'i.text**********')

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
    #         print('next')
    #         for k in range(len(nextNodeList) -2):
    #             wait = WebDriverWait(browser, 10)
    #             wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Z_list')))
    #             if len(nextNodeList) > 2:
    #                 nextNode = browser.find_element_by_xpath('//a[text()="下一页"]')
    #                 if nextNode:
    #                     resultTemp = getZiRoomListData(browser)
    #                     result.extend(resultTemp)
    #                     nextNode.click()

    print(result,'resultZi22222222222')
    
    return result

def getMyHomeListData(browser):
    result = []
    roomlist = browser.find_element_by_class_name('pList')
    items = roomlist.find_elements_by_tag_name('li')
    print(items,'items11111')

    for i in items:
        imgDiv = i.find_element_by_class_name('listImg')
        print(imgDiv,'imgDiv11111')
        detail = imgDiv.find_element_by_tag_name('a')
        detailUrl = detail.get_attribute('href')
        if detailUrl.find('http') == -1:
            detailUrl.replace('//','http://')

        img = imgDiv.find_element_by_css_selector('a>img')
        imgSrc = img.get_attribute('src')
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
            textList = pList[0].text.split('.')
            if len(textList) > 3:
                area = textList[1].strip()[::2]
                floorData = textList[3].strip().split('/')
                if len(floorData) > 1:
                    floor = floorData[0]
                    floorTotal = floorData[1]
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
    print(result,'getMyHomeListData result11111')
    return result
