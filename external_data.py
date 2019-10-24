import pandas as pd


def get_orcamento_publico(data, columns_cod):
    """http://siops-asp.datasus.gov.br/CGI/tabcgi.exe?SIOPS/serhist/municipio/mIndicadores.def
    
    """
    orcamento = pd.read_csv('../data/Orçamento_Publico_saude_2000-2018.csv', sep=';',
                                        skiprows=3, skipfooter=2, encoding='latin1')
    
    orcamento['COD_MUNICIPIO'] = orcamento['Munic-BR'].str[:6]
    orcamento = orcamento.drop('Munic-BR', 1)
    orcamento['COD_MUNICIPIO'] = pd.to_numeric(orcamento['COD_MUNICIPIO'])
    
    for col in columns_cod:
        orcamento_col = orcamento.copy()
        orcamento_col.columns = ['{0}_{1}'.format(col, x) for x in orcamento_col]
        orcamento_col[col] = orcamento_col['{0}_{1}'.format(col, 'COD_MUNICIPIO')]

        data = data.merge(orcamento_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'COD_MUNICIPIO'), 1)
    
    return data

def get_municipio_info(data, columns_cod):
    """Source: https://github.com/kelvins/Municipios-Brasileiros

    """
    municipio = pd.read_csv('../data/municipios.csv', sep=',')
    municipio.columns = [x.upper() for x in municipio.columns]

    municipio['CODIGO_IBGE'] = municipio['CODIGO_IBGE'].astype(str)
    # numero verificador removed
    municipio['CODIGO_IBGE'] = municipio['CODIGO_IBGE'].str[:-1]
    municipio['CODIGO_IBGE'] = pd.to_numeric(municipio['CODIGO_IBGE'])

    for col in columns_cod:
        municipio_col = municipio.copy()
        municipio_col.columns = [
            '{0}_{1}'.format(col, x) for x in municipio_col]
        municipio_col[col] = municipio_col['{0}_{1}'.format(
            col, 'CODIGO_IBGE')]

        data = data.merge(municipio_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'CODIGO_IBGE'), 1)

    return data


def get_cep_info(data, columns_cep):
    """Source: http://cep.la/baixar

    """
    cep_df = pd.read_csv('../data/ceps-latin1.txt', encoding='latin1',
                         sep='\t', names=['CEP', 'MUNICIPIO', 'BAIRRO', 'COMPLEMENTO'])

    cep_df['CEP'] = cep_df['CEP'].astype(str).str.zfill(8)
    cep_df = cep_df.drop('MUNICIPIO', 1)

    for col in columns_cep:
        cep_col = cep_df.copy()
        cep_col.columns = ['{0}_{1}'.format(col, x) for x in cep_col]
        cep_col[col] = cep_col['{0}_{1}'.format(col, 'CEP')]

        data = data.merge(cep_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'CEP'), 1)

    return data