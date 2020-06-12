import os
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from lib.utils.KRX import KRX


def modify(path, data_path, count):
    print('Modifying Data...')

    modified_path = os.path.join(path, 'KOSPI200_modified')

    try:
        if not os.path.exists(modified_path):
            os.makedirs(modified_path)
    except OSError:
        print('Error: Creating Directory')

    file = os.listdir(f'{data_path}')
    for f in tqdm(file, total=len(file)):
        df = pd.read_excel(f'{data_path}/{f}')

        if len(df.index) == count-1:
            df.to_excel(f'{modified_path}/{f}', index=False)
            continue

        columns = df.columns.values
        zeros = pd.Series(np.zeros(count - len(df.index) - 1))

        df_new = pd.DataFrame()
        for col in columns:
            df_new[f'{col}'] = pd.concat([zeros, df[f'{col}']])

        df_new.to_excel(f'{modified_path}/{f}', index=False)


def moving_average(path, indices, window_size):
    mov_avg = list()
    for i in tqdm(range(len(indices.index) - window_size + 1), total=len(indices.index) - window_size + 1):
        lst = list()
        for flag, value in zip(indices['fluc_tp_cd'].values[i:i + window_size], indices['cmpprevdd_idx'].values[i:i + window_size]):
            if int(flag) == 2:
                value = -float(value)
            lst.append(float(value))

        avg = np.mean(np.array(lst))
        mov_avg.append(avg)

    pd.DataFrame(mov_avg, columns=['이동평균선']).to_excel(path + '/KOSPI200_indices_moving_average.xlsx')


def download(path, start_date, end_date, window_size, name='KOSPI200'):
    krx = KRX()

    # 주말 및 KRX 휴장일
    # [calnd_dd, dy_tp_cd, calnd_dd_dy, kr_dy_tp, holdy_nm]
    sd_holiday = krx.get_holiday(start_date[:4])
    sd_holiday = sd_holiday['calnd_dd'].str.replace('-', '').values

    if start_date in sd_holiday or pd.Timestamp(start_date).day_name() in ['Saturday', 'Sunday']:
        print('Start Date is holiday or weekend.')
        exit()

    # 주말 및 KRX 휴장일
    # [calnd_dd, dy_tp_cd, calnd_dd_dy, kr_dy_tp, holdy_nm]
    ed_holiday = krx.get_holiday(end_date[:4])
    ed_holiday = ed_holiday['calnd_dd'].str.replace('-', '').values

    if end_date in ed_holiday or pd.Timestamp(end_date).day_name() in ['Saturday', 'Sunday']:
        print('End Date is holiday or weekend.')
        exit()

    data_path = os.path.join(path, name)

    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
    except OSError:
        print('Error: Creating Directory')

    # KRX 전체 기업
    # [full_code, short_code, codeName, marketName]
    company = krx.get_company()
    company.to_excel(path + '/KRX_list.xlsx')

    # KOSPI 200 기업
    # [종목코드, 종목명, 현재가, 대비, 등락률, 거래대금(원), 상장시가총액(원)]
    kospi_200 = krx.get_kospi_200(end_date)
    kospi_200.to_excel(path + '/KOSPI200_list.xlsx')

    # KOSPI 200 지수
    # [일자(trd_dd), 현재지수(clsprc_idx), 대비(fluc_tp_cd(1:+, 2:-), cmpprevdd_idx), 등락률(fluc_rt),
    # 배당수익률(div_yd), 주가이익비율(wt_per), 주가자산비율(wt_stkprc_netasst_rto), 시가지수(opnprc_idx),
    # 고가지수(hgprc_idx), 저가지수(lwprc_idx), 거래량(acc_trdvol), 거래대금(acc_trdval), 상장시가총액(mktcap)]
    kospi_200_indices = krx.get_indices(start_date, end_date)
    kospi_200_indices.drop(kospi_200_indices.index[0], inplace=True)
    kospi_200_indices.to_excel(path + '/KOSPI200_indices.xlsx')

    moving_average(path, kospi_200_indices, window_size)

    max_count = 0
    code_table = dict()

    for i in tqdm(kospi_200['종목코드'], total=len(kospi_200['종목코드'])):
        i = 'A' + str(i).zfill(6)
        code = company.loc[company['short_code'] == i, ['full_code', 'codeName']]

        code_table[code['full_code'].values[0]] = code['codeName'].values[0]

        # 기업 정보
        # [년/월/일, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주)]
        ticker = krx.get_ticker(code['full_code'], start_date, end_date)
        ticker = ticker.sort_values('년/월/일')

        if max_count < ticker.shape[0]:
            max_count = ticker.shape[0]

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

        # 대비율 = 현재 종가 / 전날 종가
        contrast_ratio = (ticker['종가'] / ticker['종가'].shift(1))
        ticker['대비율'] = contrast_ratio

        # 거래율 = 거래량 / 상장주식수
        transaction_ratio = ticker['거래량(주)'] / ticker['상장주식수(주)']
        ticker['거래율'] = transaction_ratio

        ticker.drop(ticker.index[0], inplace=True)

        ticker.to_excel('{}/{}_{}.xlsx'.format(data_path, code['full_code'].values[0], code['codeName'].values[0]), index=False)

    modify(path, data_path, max_count)

    with open('code_table.pkl', 'wb') as f:
        pickle.dump(code_table, f)
