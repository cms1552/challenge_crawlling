import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import json
import pymysql

#접수중, 접수예정, 마감임박 공모전 링크를 크롤링
# uri : 씽굿 분야별 공모전 첫 페이지
# page_num : 페이지 넘버
#반드시 첫페이지 주소를 넘겨야함
#ex) https://www.thinkcontest.com/Contest/CateField.html?c=2 이런식
def ch_crawl_link(uri, page_num=1):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    arr = list()
    over = True
    uri1 = uri[:52]
    uri3 = uri[52:]
    thinkcontest = "https://www.thinkcontest.com/"
    while(over):
        uri2 = f"page={page_num}&"
        url = uri1+uri2+uri3
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        table = soup.find('table', {"class":"type-2 mg-t-5 contest-table"})
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            deadline = tds[2].find('span', {"class":"badge status seq2"})
            deadline2 = tds[2].find('span', {"class":"badge status seq3"})
            deadline3 = tds[2].find('span', {"class":"badge status seq1"})
            #print(deadline)
            if (deadline is None and deadline2 is None and deadline3 is None):
                over = False
            link = tds[0].find("a")["href"]
            print(link)
            link = thinkcontest+link
            arr.append(link)
        page_num = page_num + 1
        time.sleep(5)
    return arr

#thinkcontest사이트의 특정 공모전 uri를 넘겨주면 주최, 응모분야 등등을 크롤링
#ch_crawl_link 와 같이 사용
#for문으로 링크 리스트주고 이 함수사용하면 타임슬립 2~3초 정도 주기(차단방지)
def ch_crawl_info(uri, field_num):
    cap_db = pymysql.connect(
        user = 'root',
        passwd = '1234',
        host = 'localhost',
        port = 3307,
        db = 'capstone2_test',
        charset='utf8'
    )    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    res = requests.get(uri, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    dic = dict()

    #제목(title)
    title = soup.find('span', {'class':'title'}).text
    dic['제목'] = title

    #이미지 다운
    stored_title = ''.join(filter(str.isalnum, title))
    imgsrc = "https://www.thinkcontest.com"+soup.find('img', {'id':'poster'})['src']
    folder_path = "C:/Users/HP/Desktop/pythonworkspace/capstone2_startup/image/"
    path = folder_path + stored_title + ".jpg"
    urllib.request.urlretrieve(imgsrc, path)
    #이미지 서버로 보냄, 그리고 file_seq 받아옴 (이후 삽입할 때 필요해서)
    file = {"uploadFile":open(path, 'rb')}
    upload_url = "http://localhost:8080/startup/uploadFile"
    response = requests.post(upload_url, files=file)
    res_json = json.loads((response.text))
    file_seq = res_json[0]['fileSeq']
    
    #나머지 정보
    content = soup.find('div', {"class":"contest-overview"})
    trs = content.find('tbody').find_all('tr')
    for tr in trs:
        th = tr.find('th').text

        if (tr.find('td').find('p') is None):
            if(tr.find('td').find('a') is not None):
                info = tr.find('td').find('a')["href"]
                dic[th] = info
            else:
                info = tr.find('td').text
                dic[th] = info
        else:
            informations = tr.find('td').find('p').find_all('span')
            info_str = str(informations[0].text)
            for n in range(1,len(informations)):
                info_str = info_str + ', ' + str(informations[n].text)
            dic[th] = info_str
    
    #challenge 테이블에 삽입
    title = ""
    host = ""
    apply_way = ""
    qualifi = ""
    award_type = ""
    period = ""
    homepage = ""
    file_seq = file_seq
    field = field_num
    
    keys = [host, apply_way, qualifi, award_type, period, homepage, title]
    dic_keys = ['주최', '접수방법', '참가자격', '시상종류', '접수기간', '홈페이지', '제목']
    for n in range(0,len(keys)):
        try:
            keys[n] = ''.join(dic[dic_keys[n]])
        except:
            keys[n] = ""

    cursor = cap_db.cursor()
    #db에 이미 있는 공모전은 삽입하지 않음
    sql = "select * from challenge where title = %s;"
    result = cursor.execute(sql, dic['제목'])
    
    if(result==0):
        sql = "INSERT INTO challenge(host, apply_way, qualifi, award_type, period, homepage, file_seq, field, title) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (keys[0], keys[1], keys[2], keys[3], keys[4], keys[5], file_seq, field, keys[6])
        cursor.execute(sql, val)
        cap_db.commit()
    else:
        pass

    cursor.close()
    return dic



#한 페이지에 10개 리스트에 담아서 마감 여부를 여부를 확인 
#접수중이면 정보 크롤링

#공모전 테이블
#<table class = "type-2 mg-t-5 contest-table">