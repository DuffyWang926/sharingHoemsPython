import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
import asyncio
import aiohttp
    
async def getEggShellData(key):
    url =  'https://www.danke.com/room/bj?search_text=' +  key
    headers = """
    Referer: https://www.danke.com/
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
    """
    headers = headers.strip().split('\n')
    headers = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
    
    # response = await get(url,headers=headers)
    # responseText = await response.text()
    # soup = BeautifulSoup(responseText,'html.parser')

    response = requests.get(url,headers=headers)
    result = []
    soup = BeautifulSoup(response.text,'html.parser')
   
    result = getEggShellListData(soup)
    return result

async def get(url,headers):
    session = aiohttp.ClientSession()
    r = await session.get(url,headers=headers)
    await session.close()
    return r
    
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

    return result
