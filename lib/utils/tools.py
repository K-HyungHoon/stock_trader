import os
import numpy as np
import pandas as pd
from tqdm import tqdm


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