import pandas as pd
from camelot.io import read_pdf


def get_table(file):
    tables = read_pdf(file+'.pdf', pages='all')
    tables[0].to_csv(file+'.csv', encoding='utf-8') 


if __name__ == '__main__':
    
      """Source: http://www.ans.gov.br/aans/noticias-ans/qualidade-da-saude/3245-ans-divulga-lista-de-hospitais-que-atendem-criterios-de-qualidade
    
    """ 
    get_table('data/acreditadas_ANS')
    get_table('data/readmissao_ANS')
    get_table('data/seguranca_ANS')