import os
import datetime
from tqdm import tqdm
from lib.utils.KRX import KRX


def download(path, name='KOSPI200'):
    data_path = os.path.join(path, name)
    # today = datetime.datetime.now().strftime('%Y%m%d')
    today = '20200515'

    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)

    except OSError:
        print('Error: Creating Directory')

    krx = KRX()

    # KRX 전체 기업
    # [full_code, short_code, codeName, marketName]
    company = krx.get_company()
    company.to_excel(path + '/KRX_list.xlsx')

    # KOSPI 200 기업
    # [종목코드, 종목명, 현재가, 대비, 등락률, 거래대금(원), 상장시가총액(원)]
    kospi_200 = krx.get_kospi_200(today)
    kospi_200.to_excel(path + '/KOSPI200_list.xlsx')

    # KOSPI 200 지수
    # [일자(trd_dd), 현재지수(clsprc_idx), 대비(fluc_tp_cd, cmpprevdd_idx), 등락률(fluc_rt),
    # 배당수익률(div_yd), 주가이익비율(wt_per), 주가자산비율(wt_stkprc_netasst_rto), 시가지수(opnprc_idx),
    # 고가지수(hgprc_idx), 저가지수(lwprc_idx), 거래량(acc_trdvol), 거래대금(acc_trdval), 상장시가총액(mktcap)]
    kospi_200_indices = krx.get_indices('20200102', today)
    kospi_200_indices.drop(kospi_200_indices.index[0], inplace=True)
    kospi_200_indices.to_excel(path + '/KOSPI200_indices.xlsx')

    for i in tqdm(kospi_200['종목코드'], total=len(kospi_200['종목코드'])):
        i = 'A' + str(i).zfill(6)
        code = company.loc[company['short_code'] == i, ['full_code', 'codeName']]

        # 기업 정보
        # [년/월/일, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주)]
        ticker = krx.get_ticker(code['full_code'], '20200102', today)
        ticker = ticker.sort_values('년/월/일')

        # 전날 종가 / 전날 시가 (Close(t-1) / Open(t-1))
        co = (ticker['종가'].shift(1) / ticker['시가'].shift(1))
        ticker['CO'] = co

        # 전날 고가 / 전날 시가 (High(t-1) / Open(t-1))
        ho = (ticker['고가'].shift(1) / ticker['시가'].shift(1))
        ticker['HO'] = ho

        # 전날 저가 / 전날 시가 (Low(t-1) / Open(t-1))
        lo = (ticker['저가'].shift(1) / ticker['시가'].shift(1))
        ticker['LO'] = lo

        # 현재 시가 / 전날 시가 (Open(t) / Open(t-1))
        oo = (ticker['시가'] / ticker['시가'].shift(1))
        ticker['OO'] = oo

        # (현재 시가 - 전날 종가) / 전날 종가
        oc = (ticker['시가'] - ticker['종가'].shift(1)) / ticker['종가'].shift(1)
        ticker['OC'] = oc

        # (현재 고가 - 현재 종가) / 현재 종가
        hc = (ticker['고가'] - ticker['종가']) / ticker['종가']
        ticker['HC'] = hc

        # (현재 저가 - 현재 종가) / 현재 종가
        lc = (ticker['저가'] - ticker['종가']) / ticker['종가']
        ticker['LC'] = lc

        # (현재 종가 - 전날 종가) / 전날 종가
        cc = (ticker['종가'] - ticker['종가'].shift(1)) / ticker['종가'].shift(1)
        ticker['CC'] = cc

        # 대비율 = 현재 대비 / 전날 종가
        contrast_ratio = (ticker['대비'] / ticker['종가'].shift(1))
        ticker['대비율'] = contrast_ratio

        # 거래율 = 거래량 / 상장주식수
        transaction_ratio = ticker['거래량(주)'] / ticker['상장주식수(주)']
        ticker['거래율'] = transaction_ratio

        ticker.drop(ticker.index[0], inplace=True)

        ticker.to_excel('{}/{}_{}.xlsx'.format(data_path, code['full_code'].values[0], code['codeName'].values[0]),
                        index=False)
