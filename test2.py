import requests
from bs4 import BeautifulSoup
import time
import urllib.request
from requests.api import head
import pymysql
from challenge_crawl import ch_crawl_info
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
#uri = "https://www.thinkcontest.com/ufiles/contest/24e02e4c56434416c32d390b47f772c3028b878d.jpg"
url = "https://www.thinkcontest.com/Contest/ContestDetail.html?id=38731"
#res = requests.get(url, headers=headers)
#soup = BeautifulSoup(res.content, 'html.parser')

dic = ch_crawl_info(url, 15)
print(dic)


