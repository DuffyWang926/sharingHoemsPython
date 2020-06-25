import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

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
