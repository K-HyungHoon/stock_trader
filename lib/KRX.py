import json
import time
import requests
import pandas as pd
from pandas import json_normalize
from io import BytesIO


def get_per(fromdata='20080101', todate='20200505', period='day', type='kospi'):
    get_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    query_str_params = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': "MKD/13/1301/13010104/mkd13010104_02",
        'type': type,
        'period_selector': period,
        'fromdate': fromdata,
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


def get_kospi(date='20010228'):
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


def get_company(date='20010228'):
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


# def get_company():
#     """
#     Reference : https://github.com/FinanceData/FinanceDataReader/
#     """
#
#     # company
#     url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
#     df_company = pd.read_html(url, header=0)[0]
#     df_company = df_company[['회사명', '종목코드']]
#
#     df_company = df_company.rename(columns={'회사명': 'name',
#                                             '종목코드': 'code'})
#
#     df_company['code'] = df_company['code'].apply(lambda x: '{:06d}'.format(x))
#
#     # market name
#     header_data = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36', }
#
#     url = f'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=COM%2Ffinder_stkisu&name=form&_={int(time.time() * 1000)}'
#     r = requests.get(url, headers=header_data)
#
#     down_url = 'http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx'
#     down_data = {
#         'mktsel': 'ALL',
#         'pagePath': '/contents/COM/FinderStkIsu.jsp',
#         'code': r.content,
#         'geFirstCall': 'Y',
#     }
#
#     r = requests.post(down_url, down_data, headers=header_data)
#     data = json.loads(r.text)
#
#     df_finder = json_normalize(data, 'block1')
#     df_finder.columns = ['fullcode', 'shortcode', 'name', 'market']
#     df_finder['code'] = df_finder['shortcode'].str[1:]
#     df_finder = df_finder[['market', 'code']]
#
#     # merge
#     df = pd.merge(df_company, df_finder, how='left', left_on='code', right_on='code')
#
#     return df