from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import trange
import re
import os

url = "https://www.law.go.kr/DRF/lawSearch.do?OC={아이디}&target=prec&type=XML"  # {}는 미사용
response = urlopen(url).read()
bs(response)
xtree = ET.fromstring(response)

totalCnt = int(xtree.find('totalCnt').text)

## 판례목록 다운로드
page = 1
rows = []
for i in trange(int(totalCnt / 20)):
    try:
        items = xtree[5:]
    except:
        break
        
    for node in items:
        판례일련번호 = node.find('판례일련번호').text
        사건명 = node.find('사건명').text
        사건번호 = node.find('사건번호').text
        선고일자 = node.find('선고일자').text
        법원명 = node.find('법원명').text
        사건종류명 = node.find('사건종류명').text
        사건종류코드 = node.find('사건종류코드').text
        판결유형 = node.find('판결유형').text
        선고 = node.find('선고').text
        판례상세링크 = node.find('판례상세링크').text

        rows.append({'판례일련번호': 판례일련번호,
                    '사건명': 사건명,
                    '사건번호': 사건번호,
                    '선고일자': 선고일자,
                    '법원명': 법원명,
                    '사건종류명': 사건종류명,
                    '사건종류코드': 사건종류코드,
                    '판결유형': 판결유형,
                    '선고': 선고,
                    '판례상세링크': 판례상세링크})
    page += 1
    url = "https://www.law.go.kr/DRF/lawSearch.do?OC={아이디}&target=prec&type=XML&page={}".format(page)
    response = urlopen(url).read()
    xtree = ET.fromstring(response)
cases = pd.DataFrame(rows)
cases.to_csv('./cases.csv', index=False)

# 판례 본문 다운로드 (약 8~90000건이기 때문에 3~4시간 소요가 됩니다.
case_list = pd.read_csv('./cases_final.csv')
contents = ['판시사항', '판결요지', '참조조문', '참조판례', '판례내용']

def remove_tag(content):
    cleaned_text = re.sub('<.*?>', '', content)
    return cleaned_text

for content in contents:
    os.makedirs('./판례/{}'.format(content), exist_ok=True)

for i in trange(len(case_list)):
    url = "https://www.law.go.kr"
    link = case_list.loc[i]['판례상세링크'].replace('HTML', 'XML')
    url += link
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

    for content in contents:
        text = xtree.find(content).text
        # 내용이 존재하지 않는 경우 None 타입이 반환되기 때문에 이를 처리해줌
        if text is None:
            text = '내용없음'
        else:
            text = remove_tag(text)
        file = './판례/' + content + '/' + xtree.find('판례정보일련번호').text + '.txt'
        with open(file, 'w') as c:
            c.write(text)
            c.close()
