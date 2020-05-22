import os
import numpy as np
import pandas as pd
from lib.data.KRX import KRX
from tqdm import tqdm


def parse():
    krx = KRX()

    # KRX 전체 기업
    # [full_code, short_code, codeName, marketName]
    company = krx.get_company()
    # company.to_excel('./KRX.xlsx')

    # KOSPI 200 기업
    # [종목코드, 종목명, 현재가, 대비, 등락률, 거래대금(원), 상장시가총액(원)]
    kospi_200 = krx.get_kospi_200('20200515')
    # kospi_200.to_excel('./KOSPI200.xlsx')

    for i in tqdm(kospi_200['종목코드'], total=len(kospi_200['종목코드'])):
        i = 'A' + str(i).zfill(6)
        code = company.loc[company['short_code'] == i, ['full_code', 'codeName']]

        # 기업의 정보
        # [날짜, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주)]
        ticker = krx.get_ticker(code['full_code'], '20200101', '20200515')
        ticker.to_csv('./KOSPI200/{}_{}.xlsx'.format(code['full_code'].values[0], code['codeName'].values[0]), index=False)


def preprocessing(root_path, save_path):
    samples = []

    for path in os.listdir(root_path):
        full_path = os.path.join(root_path, path)
        df_company = pd.read_csv(full_path)
        df_company['종목코드'] = path.split('_')[0]

        samples.append(df_company[['종목코드', '년/월/일', '시가', '고가', '저가', '종가']].values.tolist())

    samples = np.array(samples).transpose([1, 0, 2])
    np.save(save_path, samples)

    print(f"SAVED {save_path}.npy")