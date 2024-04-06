import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


proxies = { "http": None, "https": None}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-cn,zh;q=0.9,en;q=0.8,en-gb;q=0.7,en-us;q=0.6',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    'host': 'store.steampowered.com',
    'referer': 'https://store.steampowered.com/login/?redir=search%2F%3Fterm%3D&redir_ssl=1&snr=1_7_7_230_global-header',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/119.0.0.0 safari/537.36 edg/119.0.0.0',

    'sec-ch-ua-platform': "windows"
}


#替换你自己的headers
n = 5
#n代表爬取到多少页
path = 'test.csv'
#修改你的保存位置

def getgamelist(n):
    linklist=[]
    IDlist = []

    for pagenum in range(1,n):
        r = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%pagenum,headers=headers,proxies=proxies)
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup)
        soups= soup.find_all(href=re.compile(r"https://store.steampowered.com/app/"),class_="search_result_row ds_collapse_flag")
        for i in soups:
            i = i.attrs
            i = i['href']
            link = re.search('https://store.steampowered.com/app/(\d*?)/',i).group()
            ID = re.search('https://store.steampowered.com/app/(\d*?)/(.*?)/', i).group(1)
            linklist.append(link)
            IDlist.append(ID)
        print('已完成'+str(pagenum)+'页,目前共'+str(len(linklist)))
    return linklist,IDlist

def getdf(n):
    #转df
    linklist,IDlist = getgamelist(n)
    df = pd.DataFrame(list(zip(linklist,IDlist)),
               columns =['Link', 'ID'])
    df['digged'] = False
    return df


if __name__ == "__main__":
    df = getdf(n)#n代表爬取到多少页
    df.to_csv(path)#储存
