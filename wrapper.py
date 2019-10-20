import pandas as pd
import ntpath

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
    data = pd.read_csv(path, error_bad_lines=False, encoding='latin1')
    
    
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
    
        
    if 'RF- Mamógrafos' is in filename:
        rowsskip = 4
        
    else:
        rowsskip = 3
        
    data = pd.read_csv(path, sep=';', skiprows=4, encoding='latin1')
    data = data.set_index('Município')
    
    data.columns = [pd.to_datetime('{0}-{1}-01'.format(x[:4], dict_month[x[5:8]])) for x in data.columns]
    
    
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
    
    
    