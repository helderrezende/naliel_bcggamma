import pandas as pd

def get_municipio_info(data, columns_cod):
    """Data from https://github.com/kelvins/Municipios-Brasileiros
    
    """
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