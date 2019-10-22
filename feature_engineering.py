import pandas as pd

def transform_cep_in_feature(data, columns):
    """
    CEP dictionary:

    X0000-000: Região
    0X000-000: Sub-região
    00X00-000: Setor
    000X0-000: Subsetor
    0000X-000: Divisor de subsetor
    00000-XXX: Sufixo de distribuição

    """

    for col in columns:
        data[col] = data[col].astype(str).str.zfill(8)

        data['{0}_REGIAO'.format(col)] = data[col].str[:1]
        data['{0}_SUBREGIAO'.format(col)] = data[col].str[1:2]
        data['{0}_SETOR'.format(col)] = data[col].str[2:3]
        data['{0}_SUBSETOR'.format(col)] = data[col].str[3:4]
        data['{0}_DIVISOR_SUBSETOR'.format(col)] = data[col].str[3:4]
        data['{0}_SUFIXO_DISTRIBUICAO'.format(col)] = data[col].str[5:]


    return data  