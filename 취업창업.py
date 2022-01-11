import requests
from bs4 import BeautifulSoup
import time
import json
import pymysql
from requests.api import request
from challenge_crawl import ch_crawl_info, ch_crawl_link
url = "https://www.thinkcontest.com/Contest/CateField.html?c=15"
links = ch_crawl_link(url)
for link in links:
    dic = ch_crawl_info(link, 15)
    print(dic)
    time.sleep(2)

#테스트 완료