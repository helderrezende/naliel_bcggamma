import pandas as pd
import os

script_folder = os.path.dirname(os.path.abspath(__file__))

def get_municipio_info_atlas(data, columns_cod):
    """Atlas
    
    """
    atlas = pd.read_excel('{0}/data/atlas2013_dadosbrutos_pt.xlsx'.format(script_folder), sheet_name='MUN 91-00-10')
    
    atlas = atlas[atlas['ANO'] == 2010].copy()
    relevant_columns = ['Codmun6', 'GINI', 'RDPC', 'T_AGUA', 'T_BANAGUA', 'AGUA_ESGOTO',
                        'T_LIXO', 'I_ESCOLARIDADE', 'I_FREQ_PROP',
                        'IDHM', 'IDHM_E', 'IDHM_L', 'IDHM_R', 'T_SLUZ']

    atlas = atlas[relevant_columns]
    
    for col in columns_cod:
        atlas_col = atlas.copy()
        atlas_col.columns = ['{0}_{1}'.format(col, x) for x in atlas_col]
        atlas_col[col] = atlas_col['{0}_{1}'.format(col, 'Codmun6')]

        data = data.merge(atlas_col, how='left', on=col)

        data = data.drop('{0}_{1}'.format(col, 'Codmun6'), 1)

    return data

def get_orcamento_publico(data, columns_cod, column_year):
    """http://siops-asp.datasus.gov.br/CGI/tabcgi.exe?SIOPS/serhist/municipio/mIndicadores.def
    
    """
    year_files = ['2014', '2015', '2016', '2017', '2018']
    orcamento = pd.DataFrame()

    for year in year_files:
        oracamento_ano = pd.read_csv('{1}/data/orcamento_{0}.csv'.format(year, script_folder), sep=';',
                            skiprows=3, skipfooter=2, encoding='latin1')

        oracamento_ano['COD_MUNICIPIO'] = oracamento_ano['Munic-BR'].str[:6]

        oracamento_ano[column_year] = year

        orcamento = pd.concat([oracamento_ano, orcamento])
    
    orcamento = orcamento.drop(['Munic-BR', 'Freqüência', '2.10\tSUBFUNÇÕES_ADMINISTRATIVAS',
                            '2.20\tSUBFUNÇÕES_VINCULADAS', '2.21\tAtenção_Básica',
                            '2.22_Assis._Hosp._e_Ambulat.', '2.23_Sup._Profilático_Terap.',
                            '2.24_Vigilância_Sanitária', '2.25_Vigilância_Epidemiológica',
                            '2.26_Alimentação_e_Nutrição', '2.30_INFORMAÇÕES_COMPLEMENTARES',
                            'R.Impostos_e_Transf.Const', 'R.Transf.SUS', 'D.Pessoal', 'D.R.Próprios',
                            'D.Total_Saúde'
                           ], 1)
    
    orcamento.columns = [x.upper() for x in orcamento.columns]
    for col in orcamento.columns:
        orcamento[col] = orcamento[col].astype(str)
        orcamento[col] = orcamento[col].str.replace(',', '.')
        orcamento[col] = orcamento[col].apply(pd.to_numeric, errors='coerce')
    
    for col in columns_cod:
        orcamento_col = orcamento.copy()
        orcamento_col.columns = ['{0}_{1}'.format(col, x) for x in orcamento_col]
        orcamento_col[col] = orcamento_col['{0}_{1}'.format(col, 'COD_MUNICIPIO')]
        orcamento_col[column_year] = orcamento_col['{0}_{1}'.format(col, column_year)]

        data = data.merge(orcamento_col, how='left', on=[col, column_year])

        data = data.drop('{0}_{1}'.format(col, 'COD_MUNICIPIO'), 1)
        data = data.drop('{0}_{1}'.format(col, column_year), 1)
    
    return data

def get_municipio_info(data, columns_cod):
    """Source: https://github.com/kelvins/Municipios-Brasileiros

    """
    municipio = pd.read_csv('{0}/data/municipios.csv'.format(script_folder), sep=',')
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
    cep_df = pd.read_csv('{0}/data/ceps-latin1.txt'.format(script_folder), encoding='latin1',
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
    cep_df = pd.read_csv('{0}/data/tbl_cep_201908_n_log.csv'.format(script_folder))
    
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
    """Source: http://dados.gov.br/dataset/cnes
    
    """
    cnes_loc = pd.read_csv('{0}/data/cnesnone.csv'.format(script_folder))

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


def get_review_google_cnes(data, columns):
    review = pd.read_csv('{0}/data/reviews.csv'.format(script_folder), sep=';')
    review['Nota'] = review['Nota'].apply(pd.to_numeric, errors='coerca')
    review.columns = [col.upper() for col in review.columns]
    
    for col in columns:
        review_col = review.copy()
        review_col.columns = ['{0}_{1}'.format(col, x) for x in review_col]
        review_col[col] = review_col['{0}_{1}'.format(col, 'AP_CODUNI')]

        data = data.merge(review_col, how='left', on=col)
        data = data.drop('{0}_{1}'.format(col, 'AP_CODUNI'), 1)
    
    return data 