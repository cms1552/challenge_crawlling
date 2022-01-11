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



#url = "http://localhost:8080/startup/uploadFile"
#file = {"uploadFile":open('C:/Users/HP/Desktop/pythonworkspace/capstone2_startup/image/취업창업더브릿지브릿징원코리아청년파트너모집.jpg', 'rb')}
#response = requests.post(url, files=file)
#res_json = json.loads((response.text))
#file_seq = res_json[0]['fileSeq']