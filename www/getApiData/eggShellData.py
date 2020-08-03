import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
    
def getEggShellData(key):
    url =  'https://www.danke.com/room/bj?search_text=' +  key
    headers = """
    Referer: https://www.danke.com/
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
    """
    headers = headers.strip().split('\n')
    headers = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
    r = requests.get(url,headers=headers)
    statusFlag = r.status_code == 200 
    result = []
    if statusFlag :
        soup = BeautifulSoup(r.text,'html.parser')
        print(soup,soup)
        result = getEggShellListData(soup)
    return result
    
def getEggShellListData(soup):
    items = soup.findAll('div', {'class': 'r_lbx'})
    result = []
    print(items,'items')
    for i in items:
        img = i.find('img')
        imgSrc = img['src']
        titleDiv = i.find('div', {'class': 'r_lbx_cena'})
        titleNode = titleDiv.find('a')
        title = titleNode.text.strip()
        detailUrl = titleNode['href']
        detailContent = i.find('div', {'class': 'r_lbx_cenb'}).text
        detailConList = detailContent.split('|')
        area = 0
        floor = 0
        if len(detailConList) > 2:
            area = detailConList[0].strip()[-3:]
            floor = detailConList[1].strip()[:-1]

        distanceDiv = i.find('div', {'class': 'r_lbx_cena'})
        distance = distanceDiv.find('div', {'class': 'r_lbx_cena'}).text.strip()
        tagDiv = i.find('div', {'class': 'r_lbx_cenc'})
        tagDivList = tagDiv.findAll('span')
        tagList = []
        for k in tagDivList:
            tagList.append(k.text)

        priceDiv = i.find('div', {'class': 'r_lbx_moneya'})
        price = priceDiv.find('span', {'class': 'ty_b'}).text

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

        # detail = i.find('a',{'class':'pic-wrap'})
        # detailUrl = detail['href'].replace('//','http://')
        # img = i.find('img', {'class': 'lazy'})
        # imgSrc = img['src']
        # imgSrcEnd = imgSrc.replace('//','http://')
        # titleNode = i.find('h5',{'class':'title'})
        # titleNodeHref = titleNode.find('a')
        # title = titleNodeHref.text
        # description = i.find('div',{'class':'desc'})
        # descriptions = description.select('div')
        # floorData = descriptions[0].text
        # floorArr = floorData.split('|')
        # if len(floorArr) > 0:
        #     area = floorArr[0]
        #     floorTotalData = floorArr[1]
        #     floor = floorTotalData.split('/')[0]
        #     floorTotal = floorTotalData.split('/')[1].replace('层','').strip()

        # distanceNode = description.select('div',{'class':'location'})
        # distance = distanceNode[1].string.replace('\n','').replace('\t','').replace(' ','')
        # priceNodeList = i.select('span[class="num"]')
        # priceList = []
        # for k in priceNodeList:
        #     priceList.append(k['style'].replace('//','http://'))
        
        # tagNodeDiv = i.select('div[class="tag"]')
        # tagNodeSpan = tagNodeDiv[0].select('span')
        # tagList = []
        # for k in tagNodeSpan:
        #     tagList.append(k.text)

        # res = { 
        #     'imgSrc':imgSrcEnd,
        #     'title':title,
        #     'area':area,
        #     'floor':floor,
        #     'floorTotal':floorTotal,
        #     'distance':distance,
        #     'price':priceList,
        #     'tagList':tagList,
        #     'detailUrl':detailUrl
            
        #     }
        # result.append(res)
    return result
