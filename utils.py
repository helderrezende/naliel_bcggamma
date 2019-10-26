import pandas as pd
import numpy as np
import geopy.distance

def get_relevant_columns(data):
    """Get only columns with at least 10% of rows.

    """
    count_non_nan = data.notnull().sum()
    count_non_nan = count_non_nan[count_non_nan > len(data) * 0.1]

    return count_non_nan.index


def drop_columns_with_same_value(data):
    nunique = data.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    data = data.drop(cols_to_drop, axis=1)

    return data


def create_year_month_date(data, columns):
    for col in columns:
        data['{0}_YEAR_MONTH'.format(col)] = data[col].apply(lambda x: '{0}-{1}-01'.format(x.year, str(x.month).zfill(2)))
    
    return data


def get_number_month(month):
    dict_month = {'Jan': 1,
                  'Fev': 2,
                  'Mar': 3,
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


def transform_str_to_datetime(data, columns, format_dt, dayfirst):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(8)
        data[col] = pd.to_datetime(
            data[col], dayfirst=dayfirst, format=format_dt, errors='coerce')

    return data


def transform_float_to_datetime(data, columns, format_dt, dayfirst):
    for col in columns:
        data[col] = data[col].astype(str)
        data[col] = data[col].str.zfill(10)
        data[col] = pd.to_datetime(
            data[col], dayfirst=dayfirst, format=format_dt, errors='coerce')

    return data


def _get_value_df(data, MUN, DATE):
    try:
        result = data.loc[MUN, DATE]
        
    except:
        result = np.nan
        
    return result

def calc_distance_lat_long(LAT1, LONG1, LAT2, LONG2):
    dist_1 = (LAT1, LONG1)
    dist_2 = (LAT2, LONG2)
    
    try:
        result = round(geopy.distance.vincenty(dist_1, dist_2).km, 2)
    except:
        result = np.nan
        
    return result
    