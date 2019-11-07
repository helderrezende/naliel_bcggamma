import pandas as pd
import ntpath
import utils
import feature_engineering
import external_data

import os

script_folder = os.path.dirname(os.path.abspath(__file__))

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
    data = data.reset_index()

    return data

def read_csv_rf_rh(path):
    """Files:

    RF- Leitos de Internação.csv
    RF- Mamógrafos.csv
    RF- Raios X.csv
    RF- Tomógrafos Computadorizados.csv
    RF-Ressonância Magnética.csv
    RH- Médicos.csv
    RH- Enfermeiros.csv

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
    data = data.reset_index()

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
    data = data.drop(useless_columns, 1) # drop all columns with all values NaN
    data = data.dropna(axis=1, how='all')
    data = utils.drop_columns_with_same_value(data)

    relevant_col = utils.get_relevant_columns(data)
    data = data[relevant_col].copy()

    if method == 'radioterapia':
        columns_float_to_dt = ['AP_DTSOLIC', 'AP_DTAUT',
                               'AR_INIAR1', 'AR_FIMAR1', 'AP_DTOCOR']
        
        columns_int_to_dt = ['AP_MVM', 'AP_CMP']

        columns_str_to_dt = ['AP_DTINIC', 'AR_DTIDEN',
                             'AR_DTINTR', 'AP_DTFIM']

    else:
        data = data.rename(columns={'AQ_DTIDEN': 'AR_DTIDEN', 'AQ_ESTADI':'AR_ESTADI'})
        
        columns_float_to_dt = ['AP_DTSOLIC', 'AP_DTAUT']
        
        columns_int_to_dt = ['AP_MVM', 'AP_CMP']

        columns_str_to_dt = ['AP_DTINIC', 'AP_DTFIM',
                             'AQ_DTINTR', 'AR_DTIDEN']

    data = utils.transform_float_to_datetime(data, columns_float_to_dt,
                                             '%Y%m%d.0', False)
    
    data = utils.transform_int_to_datetime(data, columns_int_to_dt,
                                             '%Y%m', False)

    data = utils.transform_str_to_datetime(data, columns_str_to_dt,
                                           '%Y%m%d', False)

    return data


def _merge_by_year_and_month(data, ext_data, type_csv):
    data['AR_DTIDEN_YEAR_MONTH'] = pd.to_datetime(data['AR_DTIDEN_YEAR_MONTH'])
    
    for ext_file in ext_data.keys():
        if type_csv == 'estabelecimento':
            ext_df = read_csv_estabelecimentos('{1}/data/{0}'.format(ext_file, '..'))
            
        elif type_csv == 'rf_rh':
            ext_df = read_csv_rf_rh('{1}/data/{0}'.format(ext_file, script_folder))
        
        column_name = ext_data[ext_file]
        
        ext_df = ext_df.melt(id_vars=["COD_MUNICIPIO"], 
                                var_name="AR_DTIDEN_YEAR_MONTH", 
                                value_name=column_name)
        
        ext_df = ext_df.rename(columns={'COD_MUNICIPIO': 'AP_UFMUN'})
        
        data = data.merge(ext_df, on=['AP_UFMUN', 'AR_DTIDEN_YEAR_MONTH'], how='left')
        
    return data

def read_sia_model(path, method):
    """ DataFrame SIA used to train
    
    """
    
    ESTABELECIMENTO_FILES = {'Estabelecimentos- Clínicas-Ambulatórios Especializados.csv' : 'CLINICAS_AMB_ESPECIALIZADO',
                              'Estabelecimentos- Hospital Especializado.csv': 'HOSPITAL_ESPECIALIZADO',
                              'Estabelecimentos- Hospital Geral.csv': 'HOSPITAL_GERAL',
                              'Estabelecimentos- Unidade Básica de Saúde.csv': 'UN_BASICA_SAUDE',
                              'Estabelecimentos- Unidade de Serviço de Apoio ao Diagnose e Terapia.csv': 'UN_DIAG_TERAPIA'}
    
    RF_RH_FILES = {'RF- Leitos de Internação.csv':  'LEITOS_INTERNACAO',
                'RF- Mamógrafos.csv': 'MAMOGRAFOS',
                'RF- Raios X.csv': 'RAIO_X',
                'RF- Tomógrafos Computadorizados.csv': 'TOMAGRAFOS',
                'RF-Ressonância Magnética.csv': 'RESSONANCIA_MAGNETICA',
                'RH- Médicos.csv': 'MEDICOS',
                'RH- Enfermeiros.csv': 'ENFERMEIROS'
                  }
    
    print ('Reading csv...')
    data = read_csv_sia(path, method)
    
    print ('Transforming csv to train...')
    data = data[data['AP_TPAPAC'] == 1] # removes data that are not from the first authorization

    data = data[data['AR_DTIDEN'] >= pd.to_datetime('2014-01-01')].copy() # filter date: date >= 2014-01-01
    
    data = feature_engineering.get_delay_tratamento(data)
    data = feature_engineering.transform_cep_in_feature(data, ['AP_CEPPCN'])
    #data = feature_engineering.label_encoder(data, ['AP_SEXO'])

    data = external_data.get_municipio_info(data, ['AP_MUNPCN', 'AP_UFMUN'])
    data = external_data.get_municipio_info_atlas(data, ['AP_MUNPCN'])
    
    data = external_data.get_cep_info(data, ['AP_CEPPCN'])
    data = external_data.get_cnes_loc(data, ['AP_CODUNI']) 
    
    #data = external_data.get_review_google_cnes(data, ['AP_CODUNI'])
    
    data = utils.create_year_month_date(data, ['AR_DTIDEN'])
    data = utils.create_year_date(data, ['AR_DTIDEN'])
    
    data = external_data.get_orcamento_publico(data, ['AP_MUNPCN'], 'AR_DTIDEN_YEAR') 
    
    data = _merge_by_year_and_month(data, ESTABELECIMENTO_FILES, 'estabelecimento')
    data = _merge_by_year_and_month(data, RF_RH_FILES, 'rf_rh')

    data['DISTANCE_HOSPITAL'] = data.apply(lambda x: utils.calc_distance_lat_long(x['AP_CEPPCN_LATITUDE'],
                                                                                    x['AP_CEPPCN_LONGITUDE'],
                                                                                    x['AP_CODUNI_LATITUDE'],
                                                                                    x['AP_CODUNI_LONGITUDE']), 1)
    
    
    data = feature_engineering.get_ratio_columns(data, ['CLINICAS_AMB_ESPECIALIZADO', 'HOSPITAL_ESPECIALIZADO',
                                                        'HOSPITAL_GERAL',  'UN_BASICA_SAUDE',
                                                        'UN_DIAG_TERAPIA', 'LEITOS_INTERNACAO',
                                                        'MAMOGRAFOS', 'RAIO_X', 'TOMAGRAFOS', 'RESSONANCIA_MAGNETICA',
                                                        'MEDICOS', 'ENFERMEIROS', 'AP_MUNPCN_pesoRUR'], 'AP_MUNPCN_POPULAÇÃO')
    
    #data = feature_engineering.creates_new_features_sia(data)
    
    return data


def read_csv_cnes(path):
    data = pd.read_csv(path, sep=';', encoding='latin1')

    return data