import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

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

lottoDf_list = []

for count in range(1, 1117):
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




