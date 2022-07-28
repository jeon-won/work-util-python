import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime

GAP = 10000 # 매매-전세 갭 일정 금액 이하 자료 조사(만원 단위)
YEAR_MONTH = 202207
SERVICE_KEY = 'GONG_GONG_DATA_PORTAL_DECODED_SEVICE_KEY'
SEOUL_GU_CODE = {
    '강남구': '11680',
    '강동구': '11740',
    '강북구': '11305',
    '강서구': '11500', 
    '관악구': '11620', 
    '광진구': '11215', 
    '구로구': '11530', 
    '금천구': '11545', 
    '노원구': '11350', 
    '도봉구': '11320', 
    '동대문구': '11230',
    '동작구': '11590', 
    '마포구': '11440', 
    '서대문구': '11410',
    '서초구': '11650', 
    '성동구': '11200', 
    '성북구': '11290', 
    '송파구': '11710', 
    '양천구': '11470', 
    '영등포구': '11560',
    '용산구': '11170', 
    '은평구': '11380', 
    '종로구': '11110', 
    '중구': '11140',
    '중랑구': '11260'  
}

def get_apt_trade_data(service_key, lawd_cd, deal_ymd):
    """
    - 아파트매매 실거래자료(XML)를 반환합니다.
    - 사용 API 안내: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058017
    Args:
        - service_key (str): 디코딩된 공공데이터 포털 일반 인증키
        - lawd_cmd (str): 각 지역별 코드
        - deal_ymd (str): 월 단위 신고자료
    
    Return:
        <class 'bytes'>
    """

    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
    params = {'serviceKey': service_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ymd}
    response = requests.get(url, params=params)
    return response.content

def get_apt_rent_data(service_key, lawd_cd, deal_ymd):
    """
    - 아파트 전월세자료(XML)를 반환합니다.
    - 사용 API 안내: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058747
    Args:
        - service_key (str): 디코딩된 공공데이터 포털 일반 인증키
        - lawd_cmd (str): 각 지역별 코드
        - deal_ymd (str): 월 단위 신고자료
    
    Return:
        <class 'bytes'>
    """
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent'
    params = {'serviceKey': service_key, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ymd}
    response = requests.get(url, params=params)
    return response.content

def get_apt_trade_list(data):
    """
    아파트매매 실거래자료(XML)를 받아 파싱된 리스트를 반환합니다.

    Args: data (<class 'bytes'>). 공공데이터 포털 API를 통해 받아온 데이터.

    Return: <class 'list'>
    """
    # xml 데이터 중 item 태그 전체를 가져옴
    soup = BeautifulSoup(data, 'xml')
    items = soup.find_all('item')

    # 각 item 태그 파싱 후 배열에 저장
    trade_list = []
    for item in items:
        dic = {}
        dic['년'] = item.find('년').string
        dic['월'] = item.find('월').string
        dic['일'] = item.find('일').string
        dic['법정동'] = item.find('법정동').string
        dic['아파트'] = item.find('아파트').string
        dic['전용면적'] = item.find('전용면적').string
        dic['거래금액'] = int(item.find('거래금액').string.replace(",", "").replace(" ", ""))
        trade_list.append(dic)

    return trade_list

def get_apt_rent_list(data):
    """
    아파트매매 전월세자료(XML)를 받아 파싱된 리스트를 반환합니다.

    Args: data (<class 'bytes'>). 공공데이터 포털 API를 통해 받아온 데이터.

    Return: <class 'list'>
    """
    # xml 데이터 중 item 태그 전체를 가져옴
    soup = BeautifulSoup(data, 'xml')
    items = soup.find_all('item')

    # 각 item 태그 파싱 후 배열에 저장
    rent_list = []
    for item in items:
        dic = {}
        dic['년'] = item.find('년').string
        dic['월'] = item.find('월').string
        dic['일'] = item.find('일').string
        dic['법정동'] = item.find('법정동').string
        dic['아파트'] = item.find('아파트').string
        dic['전용면적'] = item.find('전용면적').string
        dic['보증금액'] = int(item.find('보증금액').string.replace(",", "").replace(" ", ""))
        dic['월세금액'] = int(item.find('월세금액').string.replace(",", "").replace(" ", ""))
        rent_list.append(dic)
    
    return rent_list

def save_to_xlsx(data):
    """
    매매-전세갭 자료를 엑셀 파일(xlsx)로 저장합니다.

    Args: data (<class 'list'>): 매매-전세갭 자료

    Return: None
    """
    # 워크북 및 워크시트 생성
    wb = Workbook()
    ws = wb.active

    # 틀 고정 및 컬럼 명 찍기
    ws.freeze_panes = "A2"
    ws.append(['년월', '구', '동', '아파트명', '전용면적', '거래금액', '전세가', '매매-전세갭'])

    # 데이터 기록
    for item in data:
        ws.append([item['년월'], item['구'], item['동'], item['아파트명'], item['전용면적'], item['거래금액'], item['전세가'], item['매매-전세갭']])
    
    # 엑셀 파일저장
    date = f"gap_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}"
    file_name = f"{date}.xlsx"
    wb.save(file_name)
    wb.close()
    print(f'{file_name} 저장 완료!')


# 매매-전세 갭 자료를 gap_data 배열에 담을 거임
gap_data = []
print(f"{YEAR_MONTH} 매매-전세 갭이 {GAP}만원 이하인 서울시 아파트 내역을 조사합니다.")

# 서울시 모든 자치구 조사
for gu in SEOUL_GU_CODE: 
    # 아파트 전월세자료 및 실거래자료 얻어오기
    apt_rent_list = get_apt_rent_list(get_apt_rent_data(SERVICE_KEY, SEOUL_GU_CODE[gu], YEAR_MONTH))
    apt_trade_list = get_apt_trade_list(get_apt_trade_data(SERVICE_KEY, SEOUL_GU_CODE[gu], YEAR_MONTH))

    # 아파트 전월세자료와 실거래자료 비교
    for item_rent in apt_rent_list:
        for item_trade in apt_trade_list:
            # 두 자료 비교를 위한 인덱스 생성
            index_rent = f"{item_rent['법정동']} {item_rent['아파트']} {item_rent['전용면적']}"
            index_trade = f"{item_trade['법정동']} {item_trade['아파트']} {item_trade['전용면적']}"
            
            # 전세만 추려내서
            if(index_rent == index_trade and item_rent['월세금액'] == 0):
                # 매매-전세 갭이 일정 금액 이하인 자료를 배열에 저장
                gap = item_trade['거래금액'] - item_rent['보증금액']
                if(gap <= GAP):
                    dic = {}
                    dic['년월'] = YEAR_MONTH
                    dic['구'] = gu
                    dic['동'] = item_trade['법정동']
                    dic['아파트명'] = item_trade['아파트']
                    dic['전용면적'] = item_trade['전용면적']
                    dic['거래금액'] = item_trade['거래금액']
                    dic['전세가'] = item_rent['보증금액']
                    dic['매매-전세갭'] = gap
                    gap_data.append(dic)
                    print(dic)

# 매매-전세 갭 자료를 엑셀 파일로 저장
save_to_xlsx(gap_data)
