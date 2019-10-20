import pandas as pd

def drop_columns_with_same_value(data):
    nunique = data.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    data = data.drop(cols_to_drop, axis=1)
    
    return data


def get_number_month(month):
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
    
    
    return dict_month[month]