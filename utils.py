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

def tranform_str_to_datetime(data, columns, format_dt, dayfirst):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(8)
        data[col] = pd.to_datetime(data[col], dayfirst=dayfirst, format=format_dt, errors='coerce')
   
    return data

def tranform_float_to_datetime(data, columns, format_dt, dayfirst):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(10)
        data[col] = pd.to_datetime(data[col], dayfirst=dayfirst, format=format_dt, errors='coerce')
   
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