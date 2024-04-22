import pymysql
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

dbConn = pymysql.connect(host='localhost',user='root',password='12345', db='lottodb')

sql = "select * from lotto_tbl"

cur = dbConn.cursor()
cur.execute(sql)

dbResult = cur.fetchall()

lotto_df = pd.DataFrame(dbResult, columns=['회차','추첨일','당첨번호1','당첨번호2','당첨번호3'
    ,'당첨번호4','당첨번호5','당첨번호6','보너스번호',])

lotto_df['추첨일'] = pd.to_datetime(lotto_df['추첨일']) # 추첨일을 pandas 날짜형식으로 변환

# 추첨일에서 월(month)만 추출하여 새로운 필드로 데이터프레임에 추가

lotto_df['추첨월'] = lotto_df['추첨일'].dt.month

# lotto_month_01 = lotto_df[lotto_df['추첨월'] == 1]  # 1월에 출현했던 번호 데이터
#
# print(lotto_month_01)
#
# month01_lottolist = list(lotto_month_01['당첨번호1'])+list(lotto_month_01['당첨번호2'])+list(lotto_month_01['당첨번호3'])+list(lotto_month_01['당첨번호4'])+list(lotto_month_01['당첨번호5'])+list(lotto_month_01['당첨번호6'])+list(lotto_month_01['보너스번호'])
#
# n_lotto_data = Counter(month01_lottolist)
# # 빈도수 계산 모듈 사용
#
# print(n_lotto_data)
#
# data = pd.Series(n_lotto_data)
# data.plot(figsize=(20,30),kind='barh', grid=True, title="1월 로또 번호 빈도수")

for month in range(1, 13): # 1월 ~ 12월까지 반복
    lotto_month_df = lotto_df[lotto_df['추첨월'] == month]  # month월에 출현했던 번호 데이터프레임(1~12)
    month_lottolist = list(lotto_month_df['당첨번호1']) + list(lotto_month_df['당첨번호2']) + list(
        lotto_month_df['당첨번호3']) + list(lotto_month_df['당첨번호4']) + list(lotto_month_df['당첨번호5']) + list(
        lotto_month_df['당첨번호6']) + list(lotto_month_df['보너스번호'])
    month_freq = Counter(month_lottolist)  # 월별 출현 숫자의 빈도수

    data = pd.Series(month_freq)
    sorted_data = data.sort_values(ascending=False)  # 빈도수의 내림차순으로 정렬
    top10_data = sorted_data.head(10)  # 빈도수가 높은순으로 10개만 추출

    plt.subplot(4, 3, month)
    plt.subplots_adjust(left=0.125,bottom=0.1,right=0.9,top=0.9,wspace=0.3,hspace=0.5)

    top10_data.plot(figsize=(10,20),kind='barh',grid=True,title="월별 최다 출현 로또 번호 ")
    plt.title(f"{month}월 최다 출현 번호")
    plt.xlabel("빈도수")
    plt.ylabel("로또번호")






plt.show()
cur.close()
dbConn.close()


