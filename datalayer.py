import pandas as pd
import ntpath
import utils
import feature_engineering
import external_data

def read_csv_estabelecimentos(path):
    """Files: 
    Estabelecimentos- Clínicas-Ambulatórios Especializados.csv
    Estabelecimentos- Hospital Especializado.csv
    Estabelecimentos- Hospital Geral.csv
    Estabelecimentos- Unidade Básica de Saúde.csv
    Estabelecimentos- Unidade de Serviço de Apoio ao Diagnose e Terapia.csv

    """
    data = pd.read_csv(path, sep=';', skiprows=4, skipfooter=10, encoding='latin1')
    
    data['COD_MUNICIPIO'] = data['Município'].str[:6]
    data = data.drop('Município', 1)
    data['COD_MUNICIPIO'] = pd.to_numeric(data['COD_MUNICIPIO'])
    
    data = data.set_index('COD_MUNICIPIO')
    
    data.columns = [pd.to_datetime(
                '{0}-{1}-01'.format(x[:4], utils.get_number_month(x[5:8]))) for x in data.columns]
    
    data = data.replace('-', '0')
    data = data.apply(pd.to_numeric)

    return data

def read_csv_rf(path):
    """Files:

    RF- Leitos de Internação.csv
    RF- Mamógrafos.csv
    RF- Raios X.csv
    RF- Tomógrafos Computadorizados.csv
    RF-Ressonância Magnética.csv

    """

    filename = ntpath.basename(path)

    if 'Leitos de Internação' in filename:
        rowsskip = 3
        footerrows = 13

    else:
        rowsskip = 4
        footerrows = 10

    data = pd.read_csv(path, sep=';', skiprows=rowsskip, skipfooter=footerrows, encoding='latin1')
    
    data['COD_MUNICIPIO'] = data['Município'].str[:6]
    data = data.drop('Município', 1)
    data['COD_MUNICIPIO'] = pd.to_numeric(data['COD_MUNICIPIO'])
    
    data = data.set_index('COD_MUNICIPIO')

    data.columns = [pd.to_datetime(
        '{0}-{1}-01'.format(x[:4], utils.get_number_month(x[5:8]))) for x in data.columns]
    
    data = data.replace('-', '0')
    data = data.apply(pd.to_numeric)

    return data

def read_csv_sim(path):
    """Files:

    Mortalidade Colon e Reto SIM-SUS.csv
    Mortalidade Linfoma de Hodgkin SIM-SUS.csv
    Mortalidade Linfoma não Hodgkin SIM-SUS.csv
    Mortalidade Mama SIM-SUS.csv
    Mortalidade Prostata SIM-SUS.csv
    Mortalidade Pulmão SIM-SUS.csv


    """
    useless_columns = ['VERSAOSCB', 'VERSAOSIST', 'Unnamed: 0', 'HORAOBITO']

    data = pd.read_csv(path, error_bad_lines=False, encoding='latin1')
    data = data.drop(useless_columns, 1) # drop all columns with all values NaN
    data = data.dropna(axis=1, how='all')
    data = utils.drop_columns_with_same_value(data)

    relevant_col = utils.get_relevant_columns(data)
    data = data[relevant_col].copy()

    data = utils.transform_float_to_datetime(data, ['DTNASC', 'DTCADASTRO',
                                                    'DTRECORIGA', 'DTRECEBIM',
                                                    'DTATESTADO'], '%d%m%Y.0', True)

    data = utils.transform_str_to_datetime(data, ['DTOBITO'], '%d%m%Y', True)

    return data

def read_csv_sia(path, method):
    """Files:

    Colon e reto Quimioterapia SIA-SUS.csv
    Colon e reto Radioterapia SIA-SUS.csv
    Linfomas Quimioterapia SIA-SUS.csv
    Linfomas Radioterapia SIA-SUS.csv
    Mama Quimioterapia SIA-SUS.csv
    Mama Radioterapia SIA-SUS.csv
    Prostata Quimioterapia SIA-SUS.csv
    Prostata Radioterapia SIA-SUS.csv
    Pulmão Quimioterapia SIA-SUS.csv
    Pulmão Radioterapia SIA-SUS.csv


    """
    useless_columns = ['Unnamed: 0']

    data = pd.read_csv(path, error_bad_lines=False, encoding='latin1')
    data = data.drop(useless_columns, 1)
    # drop all columns with all values NaN
    data = data.dropna(axis=1, how='all')
    data = utils.drop_columns_with_same_value(data)

    relevant_col = utils.get_relevant_columns(data)
    data = data[relevant_col].copy()

    if method == 'radioterapia':
        columns_float_to_dt = ['AP_DTSOLIC', 'AP_DTAUT',
                               'AR_INIAR1', 'AR_FIMAR1', 'AP_DTOCOR']

        columns_str_to_dt = ['AP_DTINIC', 'AR_DTIDEN',
                             'AR_DTINTR', 'AP_DTFIM']

    else:
        columns_float_to_dt = ['AP_DTSOLIC', 'AP_DTAUT']

        columns_str_to_dt = ['AP_DTINIC', 'AP_DTFIM',
                             'AQ_DTINTR', 'AQ_DTIDEN']

    data = utils.transform_float_to_datetime(data, columns_float_to_dt,
                                             '%Y%m%d.0', False)

    data = utils.transform_str_to_datetime(data, columns_str_to_dt,
                                           '%Y%m%d', False)

    return data


def _merge_by_year_and_month(data, ext_data, type_csv):
    for ext_file in ext_data.keys():
        if type_csv == 'estabelecimento':
            ext_df = read_csv_estabelecimentos('../data/{0}'.format(ext_file))
            
        elif type_csv == 'rf':
            ext_df = read_csv_rf('../data/{0}'.format(ext_file))
        
        column_name = ext_data[ext_file]
        
        data[column_name] = data.apply(lambda x: utils._get_value_df(ext_df,
                                                                     x['AP_UFMUN'],
                                                                     x['AR_DTIDEN_YEAR_MONTH']), 1)
        
    return data

def read_sia_model(path, method):
    """ DataFrame SIA used to train
    
    """
    
    ESTABELECIMENTO_FILES = {'Estabelecimentos- Clínicas-Ambulatórios Especializados.csv' : 'CLINICAS_AMB_ESPECIALIZADO',
                              'Estabelecimentos- Hospital Especializado.csv': 'HOSPITAL_ESPECIALIZADO',
                              'Estabelecimentos- Hospital Geral.csv': 'HOSPITAL_GERAL',
                              'Estabelecimentos- Unidade Básica de Saúde.csv': 'UN_BASICA_SAUDE',
                              'Estabelecimentos- Unidade de Serviço de Apoio ao Diagnose e Terapia.csv': 'UN_DIAG_TERAPIA'}
    
    RF_FILES = {'RF- Leitos de Internação.csv':  'LEITOS_INTERNACAO',
                'RF- Mamógrafos.csv': 'MAMOGRAFOS',
                'RF- Raios X.csv': 'RAIO_X',
                'RF- Tomógrafos Computadorizados.csv': 'TOMAGRAFOS',
                'RF-Ressonância Magnética.csv': 'RESSONANCIA_MAGNETICA'}
    
    
    data = read_csv_sia(path, method)
    
    data = feature_engineering.transform_cep_in_feature(data, ['AP_CEPPCN'])

    data = external_data.get_municipio_info(data, ['AP_MUNPCN', 'AP_UFMUN'])
    data = external_data.get_cep_info(data, ['AP_CEPPCN'])
    
    data = utils.create_year_month_date(data, ['AR_DTIDEN'])
    
    data = _merge_by_year_and_month(data, ESTABELECIMENTO_FILES, 'estabelecimento')
    data = _merge_by_year_and_month(data, RF_FILES, 'rf')
    
    return data


def read_csv_cnes(path):
    data = pd.read_csv(path, sep=';', encoding='latin1')

    return data