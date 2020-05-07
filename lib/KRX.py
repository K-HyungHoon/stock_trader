import requests
import pandas as pd
from io import BytesIO


def get_per(fromdate='20080101', todate='20200505', period='day', type='kospi'):
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': "MKD/13/1301/13010104/mkd13010104_02",
        'type': type,
        'period_selector': period,
        'fromdate': fromdate,
        'todate': todate,
        'pagePath': "/contents/MKD/13/1301/13010104/MKD13010104.jsp"
    }

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/contents/MKD/13/1301/13010104/MKD13010104.jsp",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df


def get_kospi200(date='20010228'):
    """
    지수
    주가지수 -> KOSPI시리즈
    """
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/03/0304/03040101/mkd03040101T3_01',
        'ind_tp_cd': '1',
        'idx_ind_cd': '028',
        'lang': 'ko',
        'compst_isu_tp': '1',
        'schdate': date,
        'pagePath': '/contents/MKD/03/0304/03040101/MKD03040101T3.jsp'
    }

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/mdi",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df


def get_ticker(fromdate='20080101', todate='20200505', code='KR7005930003'):
    """
    통계
    주식 -> 종목시세 -> 전체종목 시세
    """
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/04/0402/04020100/mkd04020100t3_02',
        'isu_cd': code,
        'fromdate': fromdate,
        'todate': todate,
        'pagePath': '/contents/MKD/04/0402/04020100/MKD04020100T3T2.jsp'
    }

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/mdi",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df


def get_comany():
    url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
    market = 'ALL'

    params = {
        'name': 'form',
        'bld': 'COM/finder_stkisu'
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers, params=params)

    params = ({'mktsel': market,
               'searchText': ""})

    params.update({'code': resp.text})

    url = "http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx"

    resp = requests.post(url, headers=headers, data=params)

    df = pd.DataFrame(resp.json()['block1'])

    return df


def get_total_price(date='20010228'):
    """
    통계
    주식 -> 종목시세 -> 전체종목 시세
    """
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/13/1302/13020101/mkd13020101',
        'market_gubun': 'ALL',
        'sect_tp_cd': 'ALL',
        'schdate': date,
        'pagePath': '/contents/MKD/13/1302/13020101/MKD13020101.jsp'
    }

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/mdi",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df


def get_reference(date):
    # No 공휴일
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    if isinstance(date, str):
        query_str_params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/13/1302/13020401/mkd13020401',
            'market_gubun': 'STK',
            'gubun': '1',
            'schdate': date,
            'pagePath': '/contents/MKD/13/1302/13020401/MKD13020401.jsp',
        }
    elif isinstance(date, list):
        query_str_params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/13/1302/13020401/mkd13020401',
            'market_gubun': 'STK',
            'gubun': '2',
            'isu_cdnm': 'A005930/삼성전자',
            'isu_cd': 'KR7005930003',
            'isu_srt_cd': 'A005930',
            'fromdate': date[0],
            'todate': date[1],
            'pagePath': '/contents/MKD/13/1302/13020401/MKD13020401.jsp',
        }
    else:
        ValueError("data is str, list")

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/contents/MKD/13/1301/13010104/MKD13010104.jsp",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df


def get_foreign_reserves(date='20010228'):
    """
    통계
    주식 -> 종목시세 -> 전체종목 시세
    """
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/13/1302/13020402/mkd13020402',
        'market_gubun': 'STK',
        'lmt_tp': '1',
        'sect_tp_cd': 'ALL',
        'schdate': date,
        'pagePath': '/contents/MKD/13/1302/13020402/MKD13020402.jsp'
    }

    header_data = {
        'User-Agent': 'Chrome/78 Safari/537',
    }

    r = requests.get(get_req_url, query_str_params, headers=header_data)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': "http://marketdata.krx.co.kr/mdi",
        'User-Agent': 'Chrome/78 Safari/537',
    }

    form_data = {
        'code': r.content
    }

    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))

    return df