import pandas as pd
from sklearn.preprocessing import LabelEncoder


def transform_cep_in_feature(data, columns):
    """CEP dictionary:

    X0000-000: Região
    0X000-000: Sub-região
    00X00-000: Setor
    000X0-000: Subsetor
    0000X-000: Divisor de subsetor
    00000-XXX: Sufixo de distribuição

    """

    for col in columns:
        data[col] = data[col].astype(str).str.zfill(8)

        data['{0}_REGIAO'.format(col)] = data[col].str[:1].astype(int)
        data['{0}_SUBREGIAO'.format(col)] = data[col].str[1:2].astype(int)
        data['{0}_SETOR'.format(col)] = data[col].str[2:3].astype(int)
        data['{0}_SUBSETOR'.format(col)] = data[col].str[3:4].astype(int)
        data['{0}_DIVISOR_SUBSETOR'.format(
            col)] = data[col].str[3:4].astype(int)
        data['{0}_SUFIXO_DISTRIBUICAO'.format(
            col)] = data[col].str[5:].astype(int)

    return data


def label_encoder(data, encode_columns):
    """
    https://towardsdatascience.com/one-hot-encoding-is-making-your-tree-based-ensembles-worse-heres-why-d64b282b5769
    """
    for col in encode_columns:
        data[col] = data[col].fillna('NaN')

    le = LabelEncoder()
    data[encode_columns] = data[encode_columns].apply(le.fit_transform)

    return data

def get_ratio_columns(data, columns, numerator):
    for col in columns:
        data[col] = data[numerator]/data[col]
        
    return data