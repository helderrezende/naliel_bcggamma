import requests
import time
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_soup_obj(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
    except:
        soup = None

    return soup


def get_table(idEstado, idMunicipio):
    url = 'http://cnes2.datasus.gov.br/Mod_Ind_Equipamento.asp?VEstado=' + \
        idEstado+'&VMun='+idMunicipio
    soup = get_soup_obj(url)
    if(soup):
        tables = soup.find('table')
        tds = tables.find_all('td')
        lista = []
        for td in tds:
            lista.append(td.text)

        try:
            begin = lista.index('1-EQUIPAMENTOS DE DIAGNOSTICO POR IMAGEM')
        except:
            begin = 0

        try:
            end = lista.index('2-EQUIPAMENTOS DE INFRA-ESTRUTURA')
        except:
            end = 1
        important = lista[begin+1:end]

        cleaned = []
        for item in important:
            cleaned.append(item.strip('\n'))

        # Removing the last row that has only 5 fields
        table = []
        table_size = len(cleaned)-5
        for i in range(0, table_size, 6):
            table.append(cleaned[i:i+6])

        # Adding last row
        last_row = cleaned[-5:]
        last_row.insert(0, '0')
        table.append(last_row)

    else:
        table = []
    return table


def scrapping():
    root_path = 'data/equipamentos'
    os.mkdir(root_path)

    idEstado = '27'
    idMunicipio = '0010'

    url = 'http://cnes2.datasus.gov.br/Mod_Ind_Equipamento.asp?VEstado=' + \
        idEstado+'&VMun='+idEstado+idMunicipio

    soup = get_soup_obj(url)

    # Gets select options for each field
    select = soup.find_all('select')

    states = []
    options_state = select[0].find_all('option')
    for option in options_state:
        states.append({'name': option.text, 'id': option['value']})
    del states[:2]

    for state in states:
        idEstado = state['id']
        state_path = root_path+'/'+state['name']
        os.mkdir(state_path)

        url = 'http://cnes2.datasus.gov.br/Mod_Ind_Equipamento.asp?VEstado='+idEstado
        soup = get_soup_obj(url)

        select = soup.find_all('select')

        cities = []
        options_city = select[1].find_all('option')
        for option in options_city:
            cities.append({'name': option.text, 'id': option['value']})
        del cities[:1]

        for city in cities:
            idMunicipio = city['id']

#             months = []
#             options_comp = select[2].find_all('option')
#             for option in options_comp:
#                 months.append({'name': option.text, 'id': option['value']})

            table = get_table(idEstado, idMunicipio)

            if(len(table) < 6):
                table = [['0', '0', '0', '0', '0', '0']]

            df = pd.DataFrame(table,
                              columns=['Código', 'Equipamento', 'Existentes', 'Em Uso', 'Existentes SUS', 'EM uso SUS'])
            writepath = state_path+'/'+city['name']+'.csv'
            mode = 'a' if os.path.exists(writepath) else 'w'
            with open(writepath, mode, encoding='utf8') as write_file:
                df.to_csv(write_file, index=None, header=True)


if __name__ == '__main__':
    scrapping()