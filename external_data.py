import pandas as pd


def get_municipio_info_atlas(data, columns_cod):
    """Atlas
    
    """
    atlas = pd.read_excel('../data/atlas2013_dadosbrutos_pt.xlsx', sheet_name='MUN 91-00-10')
    
    atlas = atlas[atlas['ANO'] == 2010].copy()
    relevant_columns = ['Codmun6', 'GINI', 'RDPC', 'T_AGUA', 'T_BANAGUA', 'AGUA_ESGOTO',
                        'T_LIXO', 'I_ESCOLARIDADE', 'I_FREQ_PROP',
                        'IDHM', 'IDHM_E', 'IDHM_L', 'IDHM_R']

    atlas = atlas[relevant_columns]
    
    for col in columns_cod:
        atlas_col = atlas.copy()
        atlas_col.columns = ['{0}_{1}'.format(col, x) for x in atlas_col]
        atlas_col[col] = atlas_col['{0}_{1}'.format(col, 'Codmun6')]

        data = data.merge(atlas_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'Codmun6'), 1)

    return data

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


def get_cep_info_public(data, columns_cep):
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

def get_cep_info(data, columns_cep):
    cep_df = pd.read_csv('../data/tbl_cep_201908_n_log.csv')
    
    cep_df.columns = [col.upper() for col in cep_df.columns]
    
    relevant_columns = ['CEP', 'TIPO_SEM_ACENTO', 'NOME_LOGRADOURO_SEM_ACENTO',
                        'LOGRADOURO_SEM_ACENTO', 'LATITUDE', 'LONGITUDE']

    cep_df = cep_df[relevant_columns].copy()
    
    cep_df['CEP'] = cep_df['CEP'].astype(str).str.zfill(8)
    
    for col in columns_cep:
        cep_col = cep_df.copy()
        cep_col.columns = ['{0}_{1}'.format(col, x) for x in cep_col]
        cep_col[col] = cep_col['{0}_{1}'.format(col, 'CEP')]

        data = data.merge(cep_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'CEP'), 1)
    
    return data

def get_cnes_loc(data, columns_cnes):
    """http://dados.gov.br/dataset/cnes
    
    """
    cnes_loc = pd.read_csv('../data/cnesnone.csv')

    cnes_loc.columns = [col.upper() for col in cnes_loc.columns]
    cnes_loc = cnes_loc.rename(columns={'LAT': 'LATITUDE', 'LONG': 'LONGITUDE'})
    cnes_loc = cnes_loc.drop(['CO_IBGE', 'ORIGEM_DADO', 'DATA_ATUALIZACAO'], 1)
    
    for col in columns_cnes:
        cnes_col = cnes_loc.copy()
        cnes_col.columns = ['{0}_{1}'.format(col, x) for x in cnes_col]
        cnes_col[col] = cnes_col['{0}_{1}'.format(col, 'CO_CNES')]

        data = data.merge(cnes_col, how='left', on=col)
        data = data.drop('{0}_{1}'.format(col, 'CO_CNES'), 1)
    
    return data