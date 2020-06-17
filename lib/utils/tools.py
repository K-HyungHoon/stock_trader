import os
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_data(path, name='KOSPI200'):
    """
    :param
    path: CSV Folder Root Path

    :return:
    (num_company, period, feature) np.array
    """
    datas = []
    changes = []

    # 코스피 200 지수
    df_indices_mv = pd.read_excel(path + '/KOSPI200_indices_moving_average.xlsx')
    indices_mv = df_indices_mv['이동평균선'].tolist()

    with open('code_table.pkl', 'rb') as f:
        code_table = pickle.load(f)  # 단 한줄씩 읽어옴

    data_path = os.path.join(path, name)
    total_path = [os.path.join(data_path, f"{code}_{name}.xlsx") for code, name in code_table.items()]

    for full_path in tqdm(total_path, total=len(total_path)):
        df_company = pd.read_excel(full_path)

        # 기업 정보
        # [날짜, 종가, 대비, 거래량(주), 거래대금(원), 시가, 고가, 저가, 시가총액(백만), 상장주식수(주), CO, HO, LO, OO, OC, HC, LC, CC, 대비율, 거래율]
        # cdata = df_company[['OC', 'HC', 'LC', 'CC']].values * 100
        odata = (1 - df_company[['CO', 'HO', 'LO', 'OO']].values) * 100

        # data = np.concatenate((cdata, odata), axis=1)

        change = df_company['CC'].values.astype(float).tolist()

        datas.append(odata.tolist())
        changes.append(change)

    datas = np.array(datas)
    changes = np.array(changes).transpose((1, 0)) * 100

    return datas, changes, code_table, indices_mv


def save_pkl(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_pkl(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)

    return data