import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from datetime import timedelta


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
        data[col] = data[col]/data[numerator]
        
    return data

def get_delay_tratamento(data):
    delay = data[['AP_DTINIC', 'AR_DTIDEN', 'AP_CODUNI']].copy()
    delay['DELAY'] = (delay['AP_DTINIC'] - delay['AR_DTIDEN']).dt.days
    delay['DELAY'] = np.where(delay['DELAY'] < 0, np.nan, delay['DELAY'])
    
    delay = delay.sort_values('AR_DTIDEN')
    
    delay['EWM_MEAN_DELAY'] = delay.groupby(['AP_CODUNI'])['DELAY'].apply(lambda x: x.ewm(span=60, ignore_na=True).mean())
    delay['EWM_MEAN_DELAY'] = np.where(delay['DELAY'].isnull(), np.nan, delay['EWM_MEAN_DELAY'])
    
    delay['YEAR'] = delay['AR_DTIDEN'].dt.year
    delay['MONTH'] = delay['AR_DTIDEN'].dt.month
    
    delay = delay.groupby(['AP_CODUNI', 'YEAR', 'MONTH'], as_index=False)['EWM_MEAN_DELAY'].mean()
    
    data['YEAR'] = data['AR_DTIDEN'].dt.year
    data['MONTH'] = data['AR_DTIDEN'].dt.month
    
    data = data.merge(delay, on=['AP_CODUNI', 'YEAR', 'MONTH'], how='left')
    
    data = data.drop(['YEAR', 'MONTH'], 1)

    return data

def creates_new_features_sia(data):
    
    data['id'] = data['AP_CEPPCN'].apply(str) + data['AP_NUIDADE'].apply(str) + data['AP_RACACOR'].apply(str)
    
    data['AP_DTSOLIC-AUT'] = data['AP_DTSOLIC'] - data['AP_DTAUT']
    
    data['AP_OCOR_POS_MVM'] = data['AP_DTOCOR'] - data['AP_MVM']    
    data['AP_OCOR_POS_MVM'] = np.where(data['AP_OCOR_POS_MVM'] <= timedelta(days=0), 0, 1)
    
    data['AP_OCOR_VAL'] = data['AP_DTOCOR']
    data['AP_OCOR_VAL'] = np.where(data['AP_OCOR_VAL'] <= data['AP_DTFIM'], 1, 0)
    
    return data