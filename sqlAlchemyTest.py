from sqlalchemy import create_engine
import pandas as pd
import pymysql

data = {'학번': range(2000,2015), '성적':[70,60,100,90,50,75,85,99,78,63,100,77,87,78,100]}

df = pd.DataFrame(data=data, columns=['학번','성적'])

print(df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
engine.connect()
df.to_sql(name="test_tbl", con=engine, if_exists='append', index=False)





