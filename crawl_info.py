import requests
from bs4 import BeautifulSoup
import time


uri = "https://www.thinkcontest.com/Contest/ContestDetail.html?id=38731"

def ch_crawl_info(uri):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    res = requests.get(uri, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    dic = dict()
    content = soup.find('div', {"class":"contest-overview"})
    trs = content.find('tbody').find_all('tr')
    for tr in trs:
        th = tr.find('th').text

        if (tr.find('td').find('p') is None):
            info = tr.find('td').text
            dic[th] = info
        else:
            informations = tr.find('td').find('p').find_all('span')
            info_arr = list()
            for info in informations:
                info_arr.append(info.text)
            dic[th] = info_arr
    return dic
