import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import asyncio
import aiohttp
    
async def getZiRoomData(key):
    url =  'http://www.ziroom.com/z/' + '?qwd=' +  key
    urlNext = 'http://www.ziroom.com/z/z0/?qwd=' + key
    headers = """
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: max-age=0
    Connection: keep-alive
    Cookie: td_cookie=2012615485; CURRENT_CITY_CODE=110000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221739ed0acdf18b-08b5175540bf33-3323765-2073600-1739ed0ace02ab%22%2C%22%24device_id%22%3A%221739ed0acdf18b-08b5175540bf33-3323765-2073600-1739ed0ace02ab%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; gr_user_id=a7207c80-e0bb-4700-9468-178376a7abe7; td_cookie=2012573488; CURRENT_CITY_NAME=%E5%8C%97%E4%BA%AC; _csrf=xGyOZEQaY9Etv3zs6oTABSCbTTYUHZBj; Hm_lvt_4f083817a81bcb8eed537963fc1bbf10=1596097343,1596423672; gr_session_id_8da2730aaedd7628=72a8174c-1ce4-4f0b-8fc8-72c6ac1a3a95; gr_session_id_8da2730aaedd7628_72a8174c-1ce4-4f0b-8fc8-72c6ac1a3a95=true; Hm_lpvt_4f083817a81bcb8eed537963fc1bbf10=1596424291
    Host: www.ziroom.com
    Referer: http://www.ziroom.com/
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
    """
    headers = headers.strip().split('\n')
    headers = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
    
    response = await get(urlNext,headers)
    responseText = await response.text()
    result = []

    soup = BeautifulSoup(responseText,'html.parser')
    result = getZiRoomListData(soup)
    return result

async def get(url,headers):
    session = aiohttp.ClientSession()
    # proxy = 'http://175.43.58.62:9999'
    # proxy = 'http://113.195.22.169:9999'
    # proxy = 'http://125.108.119.110:9999'
    
    
    # r = await session.get(url,headers=headers, proxy=proxy)
    r = await session.get(url,headers=headers)
    await session.close()
    return r
    
def getZiRoomListData(soup):
    items = soup.findAll('div', {'class': 'item'})
    result = []
    for i in items:
        divList = i.findAll('span')
        if len(divList) > 5:
            detail = i.find('a',{'class':'pic-wrap'})
            detailUrl = detail['href'].replace('//','http://')
            img = i.find('img', {'class': 'lazy'})
            imgSrc = img['src']
            imgSrcEnd = imgSrc.replace('//','http://')
            titleNode = i.find('h5',{'class':'title'})
            titleNodeHref = titleNode.find('a')
            title = titleNodeHref.text.strip()
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
