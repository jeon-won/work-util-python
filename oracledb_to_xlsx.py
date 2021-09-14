import cx_Oracle
import pandas as pd

"""
oracledb_to_xlsx.py
* Date: 2021. 9. 14.
* Author: Jeon Won
* Func: 오라클 DB 쿼리 실행 결과를 엑셀 파일(xlsx)로 저장
* Usage: `pip install cx_Oracle pandas` 명령어로 필요한 모듈 설치 → 상수 및 변수 값 설정 후 실행
"""

# 상수 & 변수
USERNAME = 'USERNAME'
PASSWORD = 'P@SsW0rd'
IP = '192.168.0.1'
PORT = 1234
SID = 'ORACLE_SID'
query = 'SQL Query'
xlsx_name = 'test.xlsx'

# DB 연결 후 쿼리 실행 결과 얻어오기
con = cx_Oracle.connect(f'{USERNAME}/{PASSWORD}@{IP}:{PORT}/{SID}')
data = pd.read_sql(query, con)
con.close()

# xlsx 파일로 저장
data.head()
data.to_excel(xlsx_name)
print(f'{xlsx_name} Save success!')
