import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from lib.data.KRX import KRX


def parse(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)

    except OSError:
        print('Error: Creating Directory')

    krx = KRX()

    # KRX 전체 기업
    # [full_code, short_code, codeName, marketName]
    company = krx.get_company()
    # company.to_excel(path + '/KRX.xlsx')

    # KOSPI 200 기업
    # [종목코드, 종목명, 현재가, 대비, 등락률, 거래대금(원), 상장시가총액(원)]
    kospi_200 = krx.get_kospi_200('20200515')
    # kospi_200.to_excel(path + '/KOSPI200.xlsx')

    for i in tqdm(kospi_200['종목코드'], total=len(kospi_200['종목코드'])):
        i = 'A' + str(i).zfill(6)
        code = company.loc[company['short_code'] == i, ['full_code', 'codeName']]

        # 기업 정보
        # [년/월/일, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주)]
        ticker = krx.get_ticker(code['full_code'], '20190301', '20200515')
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

        # 수익률 = log(현재 종가 / 전날 종가)
        yield_ratio = np.log(ticker['종가'] / ticker['종가'].shift(1))
        ticker['수익률'] = yield_ratio

        ticker.drop(ticker.index[0], inplace=True)

        # 평균 수익률
        # 샤프 지수
        ticker.to_excel('{}/{}_{}.xlsx'.format(path, code['full_code'].values[0], code['codeName'].values[0]),
                        index=False)


def get_data(path):
    """
    :param
    path: CSV Folder Root Path

    :return:
    (num_company, period, feature) np.array
    """
    datas = []
    changes = []
    labels = []

    total_path = os.listdir(path)

    for file_name in tqdm(total_path, total=len(total_path)):
        full_path = os.path.join(path, file_name)
        df_company = pd.read_excel(full_path)
        labels.append(file_name.split('_')[0])

        # 기업 정보
        # [날짜, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주), CO, HO, LO, OO, OC, HC, LC, CC, 대비율, 거래율, 수익률]
        data = df_company[['CO', 'HO', 'LO', 'OO', '거래율', '대비율']].values.tolist()
        change = df_company['대비율'].values.astype(float).tolist()

        datas.append(data)
        changes.append(change)

    datas = np.array(datas)

    return datas, changes, labels


if __name__ == "__main__":
    root_path = 'data'
    data_path = 'KOSPI200'
    path = os.path.join(root_path, data_path)

    parse(path)