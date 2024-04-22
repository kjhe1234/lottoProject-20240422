import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql


def get_lottoNumber(count):   # 로또 추첨 회차 를 입력 받음
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find('p', {'class': 'desc'}).text  # 로또 추첨일
    lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")
    lottoNumber = soup.find('div', {'class': 'num win'}).find('p').text.strip().split('\n')
    lottoNumberList = []
    for num in lottoNumber:
        num = int(num)
        lottoNumberList.append(num)
    bonusNumber = int(soup.find('div', {'class': 'num bonus'}).find('p').text.strip())

    lottoDic = {'lottoDate': lottoDate, 'lottoNumber': lottoNumberList, 'bonusNumber': bonusNumber}

    return lottoDic

def get_recent_lottocount():  # 최신 로또 회차 크롤링 함수
    url = "https://dhlottery.co.kr/common.do?method=main"  # 동행복권 첫 페이지 사이트 주소
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    recent_count = soup.find("strong", {'id': 'lottoDrwNo'}).text.strip()
    recent_count = int(recent_count)
    return recent_count+1



lottoDf_list = []


for count in range(1, get_recent_lottocount()):
    lottoResult = get_lottoNumber(count)
    lottoDf_list.append({
        'count': count,  # 로또 추첨 회차
        'lottoDate' : lottoResult['lottoDate'], # 로또 추첨일
        'lottoNum1' : lottoResult['lottoNumber'][0],  # 로또 당첨 번호 중 첫번째 번호
        'lottoNum2' : lottoResult['lottoNumber'][1],  # 로또 당첨 번호 중 두번째 번호
        'lottoNum3': lottoResult['lottoNumber'][2],  # 로또 당첨 번호 중 세번째 번호
        'lottoNum4': lottoResult['lottoNumber'][3],  # 로또 당첨 번호 중 네번째 번호
        'lottoNum5': lottoResult['lottoNumber'][4],  # 로또 당첨 번호 중 다섯번째 번호
        'lottoNum6': lottoResult['lottoNumber'][5],  # 로또 당첨 번호 중 여섯번째 번호
        'bonusNum' : lottoResult['bonusNumber'] # 로또 보너스 번호
    })

    print(f"{count}회 처리중...")

#print(lottoDf_list)

lottoDF = pd.DataFrame(data=lottoDf_list, columns= ['count','lottoDate','lottoNum1','lottoNum2','lottoNum3'
             ,'lottoNum4','lottoNum5','lottoNum6','bonusNum'])

print(lottoDF)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
engine.connect()
lottoDF.to_sql(name="lotto_tbl", con=engine, if_exists='append', index=False)



