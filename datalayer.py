import pandas as pd
import ntpath
from utils import drop_columns_with_same_value, get_number_month, get_relevant_columns, tranform_str_to_datetime, tranform_float_to_datetime
          
def read_csv_sim(path):
    '''
    Files:
    
    Mortalidade Colon e Reto SIM-SUS.csv
    Mortalidade Linfoma de Hodgkin SIM-SUS.csv
    Mortalidade Linfoma não Hodgkin SIM-SUS.csv
    Mortalidade Mama SIM-SUS.csv
    Mortalidade Prostata SIM-SUS.csv
    Mortalidade Pulmão SIM-SUS.csv
    
    
    '''
    useless_columns = ['VERSAOSCB', 'VERSAOSIST', 'Unnamed: 0', 'HORAOBITO'] 
    
    data = pd.read_csv(path, error_bad_lines=False, encoding='latin1')
    data = data.drop(useless_columns, 1)
    data = data.dropna(axis=1, how='all') # drop all columns with all values NaN
    data = drop_columns_with_same_value(data)
    
    relevant_col = get_relevant_columns(data)
    data = data[relevant_col].copy()
    
    
    data = tranform_float_to_datetime(data,
                                      ['DTNASC', 'DTCADASTRO',
                                       'DTRECORIGA', 'DTRECEBIM',
                                       'DTATESTADO'])
    
    data = tranform_str_to_datetime(data, ['DTOBITO'])
    
    
    return data

def read_csv_sia(path):
    '''
    Files:
    
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
    
    
    '''
    useless_columns = ['Unnamed: 0'] 
    
    
    data = pd.read_csv(path, error_bad_lines=False, encoding='latin1')
    data = data.drop(useless_columns, 1)
    data = data.dropna(axis=1, how='all') # drop all columns with all values NaN
    data = drop_columns_with_same_value(data)
    
    relevant_col = get_relevant_columns(data)
    data = data[relevant_col].copy()
    
    return data

def read_csv_rf(path):
    '''
    Files:
    
    RF- Leitos de Internação.csv
    RF- Mamógrafos.csv
    RF- Raios X.csv
    RF- Tomógrafos Computadorizados.csv
    RF-Ressonância Magnética.csv
    
    '''
    
    filename = ntpath.basename(path)
    
        
    if 'Leitos de Internação' in filename:
        rowsskip = 3
        
    else:
        rowsskip = 4
        
    data = pd.read_csv(path, sep=';', skiprows=4, encoding='latin1')
    data = data.set_index('Município')
    
    data.columns = [pd.to_datetime('{0}-{1}-01'.format(x[:4], get_number_month(x[5:8]))) for x in data.columns]
    
    return data

def read_csv_estabelecimentos(path):
    '''
    Files: 
    Estabelecimentos- Clínicas-Ambulatórios Especializados.csv
    Estabelecimentos- Hospital Especializado.csv
    Estabelecimentos- Hospital Geral.csv
    Estabelecimentos- Unidade Básica de Saúde.csv
    Estabelecimentos- Unidade de Serviço de Apoio ao Diagnose e Terapia.csv

    '''
       
    data = pd.read_csv(path, sep=';', skiprows=4, encoding='latin1')
    
    
    return data