import requests
import pandas as pd
from io import BytesIO


class KRX:
    def __init__(self):
        pass

    def get_company(self):
        url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
        header = {"User-Agent": "Mozilla/5.0"}
        param = {
            'name': 'form',
            'bld': 'COM/finder_stkisu'
        }

        req = requests.get(url, headers=header, params=param)

        url = "http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx"
        param = {
            'mktsel': 'ALL',
            'searchText': ''
        }
        param.update({'code': req.text})

        req = requests.post(url, headers=header, data=param)

        df = pd.DataFrame(req.json()['block1'])
        return df

    # KRX -> 지수 -> 주가지수 -> KOSPI 시리즈
    def get_kospi_200(self, date):
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        header = {'User-Agent': 'Chrome/78 Safari/537'}
        param = {
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

        r = requests.get(url, headers=header, params=param)

        url = 'http://file.krx.co.kr/download.jspx'
        header = {
            'Referer': "http://marketdata.krx.co.kr/mdi",
            'User-Agent': 'Chrome/78 Safari/537',
        }
        param = {'code': r.content}

        r = requests.post(url, headers=header, params=param)

        df = pd.read_excel(BytesIO(r.content))
        return df

    # JJM
    def get_ticker(self, code, from_date, to_date):
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        header = {'User-Agent': 'Chrome/78 Safari/537'}
        param = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/04/0402/04020100/mkd04020100t3_02',
            'isu_cd': code,
            'fromdate': from_date,
            'todate': to_date,
            'pagePath': '/contents/MKD/04/0402/04020100/MKD04020100T3T2.jsp'
        }

        r = requests.get(url, headers=header, params=param)

        url = 'http://file.krx.co.kr/download.jspx'
        header = {
            'Referer': "http://marketdata.krx.co.kr/mdi",
            'User-Agent': 'Chrome/78 Safari/537',
        }
        param = {'code': r.content}

        r = requests.post(url, headers=header, params=param)

        df = pd.read_excel(BytesIO(r.content))
        return df

    # 통계 -> 주식 -> 종목시세 -> 전체종목 시세
    def get_total_price(self, date='20010228'):
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        header = {'User-Agent': 'Chrome/78 Safari/537'}
        param = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/13/1302/13020101/mkd13020101',
            'market_gubun': 'ALL',
            'sect_tp_cd': 'ALL',
            'schdate': date,
            'pagePath': '/contents/MKD/13/1302/13020101/MKD13020101.jsp'
        }

        r = requests.get(url, headers=header, params=param)

        url = 'http://file.krx.co.kr/download.jspx'
        header = {
            'Referer': "http://marketdata.krx.co.kr/mdi",
            'User-Agent': 'Chrome/78 Safari/537',
        }
        param = {'code': r.content}

        r = requests.post(url, headers=header, params=param)

        df = pd.read_excel(BytesIO(r.content))
        return df

    #
    def get_reference(self, date):
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

    # KRX -> 주식 -> 투자참고 -> 외국인보유량
    def get_foreign_reserves(self, date='20010228'):
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        header = {'User-Agent': 'Chrome/78 Safari/537'}
        param = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/13/1302/13020402/mkd13020402',
            'market_gubun': 'STK',
            'lmt_tp': '1',
            'sect_tp_cd': 'ALL',
            'schdate': date,
            'pagePath': '/contents/MKD/13/1302/13020402/MKD13020402.jsp'
        }

        r = requests.get(url, headers=header, params=param)

        url = 'http://file.krx.co.kr/download.jspx'
        header = {
            'Referer': "http://marketdata.krx.co.kr/mdi",
            'User-Agent': 'Chrome/78 Safari/537',
        }
        param = {'code': r.content}

        r = requests.post(url, headers=header, params=param)

        df = pd.read_excel(BytesIO(r.content))
        return df

    """
    # PER
    def get_per(self, from_date='20080101', to_date='20200505', period='day', type='kospi'):
        get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

        query_str_params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': "MKD/13/1301/13010104/mkd13010104_02",
            'type': type,
            'period_selector': period,
            'fromdate': from_date,
            'todate': to_date,
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
    """
