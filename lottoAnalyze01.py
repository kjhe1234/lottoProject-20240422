import pymysql
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
#빈도수 계산 모듈


dbConn = pymysql.connect(host='localhost',user='root',password='12345', db='lottodb')

sql = "select * from lotto_tbl"

cur = dbConn.cursor()
cur.execute(sql)

dbResult = cur.fetchall()

lotto_df = pd.DataFrame(dbResult, columns=['회차','추첨일','당첨번호1','당첨번호2','당첨번호3'
    ,'당첨번호4','당첨번호5','당첨번호6','보너스번호',])

#print(lotto_df)

lotto_num_df = pd.DataFrame(lotto_df.iloc[0:,2:])  # 당첨 번호 와 보너스 번호만 추출하여 데이터 프레임 생성

print(lotto_num_df)

lotto_num_list = list(lotto_num_df['당첨번호1'])+list(lotto_num_df['당첨번호2'])+list(lotto_num_df['당첨번호3'])+list(lotto_num_df['당첨번호4'])+list(lotto_num_df['당첨번호5'])+list(lotto_num_df['당첨번호6'])+list(lotto_num_df['보너스번호'])
print(len(lotto_num_list))

# for i in range(1, 46):
#     count = 0
#     for num in lotto_num_list:
#         if num == i:
#             count = count +1
#     print(f"{i}의 빈도수 : {count}")

n_lotto_data = Counter(lotto_num_list)
# 빈도수 계산 모듈 사용

print(n_lotto_data)

data = pd.Series(n_lotto_data)
data.plot(figsize=(20,30),kind='barh', grid=True, title="lotto KOR DATA")

plt.show()

cur.close()
dbConn.close()
