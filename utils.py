import pandas as pd

def get_relevant_columns(data):
    """
    Get only columns with at least 10% of rows.
    
    """
    count_non_nan = data.notnull().sum()
    count_non_nan = count_non_nan[count_non_nan > len(data) * 0.1]
    
    return count_non_nan.index

def drop_columns_with_same_value(data):
    nunique = data.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    data = data.drop(cols_to_drop, axis=1)
    
    return data

def get_number_month(month):
    dict_month = {'Jan' : 1,
              'Fev' : 2,
              'Mar' : 3,
              'Abr': 4,
              'Mai': 5,
              'Jun': 6,
              'Jul': 7,
              'Ago': 8,
              'Set': 9,
              'Out': 10,
              'Nov': 11,
              'Dez': 12}
    
    return dict_month[month]

def tranform_str_to_datetime(data, columns):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(8)
        data[col] = pd.to_datetime(data[col], dayfirst=True, format='%d%m%Y')
   
    return data


def tranform_float_to_datetime(data, columns):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(10)
        data[col] = pd.to_datetime(data[col], dayfirst=True, format='%d%m%Y.0', errors='coerce')
   
    return data


def get_municipio_info(data, columns_cod):
    municipio = pd.read_csv('../data/municipios.csv', sep=',')

    municipio['codigo_ibge'] = municipio['codigo_ibge'].astype(str)
    municipio['codigo_ibge'] = municipio['codigo_ibge'].str[:-1] # numero verificador removed
    municipio['codigo_ibge'] = pd.to_numeric(municipio['codigo_ibge'])


    for col in columns_cod:
        municipio_col = municipio.copy()
        municipio_col.columns = ['{0}_{1}'.format(col, x) for x in municipio_col]
        municipio_col[col] = municipio_col['{0}_{1}'.format(col, 'codigo_ibge')]

        data = data.merge(municipio_col, how='left', on=col) 

        data = data.drop('{0}_{1}'.format(col, 'codigo_ibge'), 1)
    
    return data
    
    
def trasnform_cep_in_feature(data, columns):
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
    