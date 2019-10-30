import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, roc_auc_score
import shap
import numpy as np
import pandas as pd
from datalayer import read_sia_model

def get_train_and_test_data(data):
    data['AR_ESTADI'] = data['AR_ESTADI'].apply(pd.to_numeric, errors='coerce')
    data = data.dropna(subset=['AR_ESTADI'])
    
    data['AR_ESTADI'] = np.where(data['AR_ESTADI'] <= 2, 0, 1)
    
    
    X_with_cep = data[['AP_CEPPCN', 'AP_MUNPCN_CODIGO_UF', 'AP_MUNPCN_NOME',
              'CLINICAS_AMB_ESPECIALIZADO', 'HOSPITAL_ESPECIALIZADO', 'HOSPITAL_GERAL', 
              'UN_BASICA_SAUDE', 'UN_DIAG_TERAPIA', 'LEITOS_INTERNACAO', 'MAMOGRAFOS',
              'RAIO_X', 'TOMAGRAFOS', 'RESSONANCIA_MAGNETICA',
              'AP_MUNPCN_GINI', 'AP_MUNPCN_RDPC', 'AP_MUNPCN_T_AGUA',
              'AP_MUNPCN_AGUA_ESGOTO',
              'AP_MUNPCN_T_BANAGUA', 'AP_MUNPCN_T_LIXO', 'AP_MUNPCN_I_ESCOLARIDADE',
              'AP_MUNPCN_I_FREQ_PROP', 'AP_MUNPCN_IDHM', 'AP_MUNPCN_IDHM_E', 
              'AP_MUNPCN_IDHM_L', 'AP_MUNPCN_T_SLUZ',
              'EWM_MEAN_DELAY',
              'AP_MUNPCN_IDHM_R', 'MEDICOS', 'ENFERMEIROS', 'DISTANCE_HOSPITAL',
              'AP_MUNPCN_1.1_%R.LÍQUIDA_TOTAL',
              'AP_MUNPCN_1.2_%TRANSF._INTERGOV._LÍQUIDAS',
              'AP_MUNPCN_1.3_%TRANSF._PARA_A_SAÚDE_(SUS)', 'AP_MUNPCN_1.4_%TRANSF._UNIÃO_P/_SAÚDE',
              'AP_MUNPCN_1.5_%TRANSF._DA_UNIÃO_P/_(SUS)',
              'AP_MUNPCN_1.6_%R.IMP._TRANSF.CONST.LEGAIS',
              'AP_MUNPCN_2.1_D.TOTAL_SAÚDE/HAB', 
              'AP_MUNPCN_2.2_%D.PESSOAL/D.TOTAL',
              'AP_MUNPCN_2.3_%D.COM_MEDICAMENTOS',
              'AP_MUNPCN_2.4_%D.SERV.TERC/D.TOTAL',
              'AP_MUNPCN_2.5_%D.INVEST/D.TOTAL',
              'AP_MUNPCN_3.1_%TRANSF.SUS/D.TOTAL', 
              'AP_MUNPCN_3.2_%R.PRÓPRIOS_EM_SAÚDE-EC_29', 
              'AP_MUNPCN_R.TRANSF.SUS/HAB', 
              'AP_MUNPCN_D.R.PRÓPRIOS_EM_SAÚDE/HAB'
             ]]
    
    X = X_with_cep.drop(['AP_CEPPCN', 'AP_MUNPCN_CODIGO_UF', 'AP_MUNPCN_NOME'], 1)

    y = data['AR_ESTADI']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    
    d_train = xgb.DMatrix(X_train, label=y_train)
    d_test = xgb.DMatrix(X_test, label=y_test)
    
    return X, X_with_cep, y, y_test, d_train, d_test

def train_sia(data):
    X, X_with_cep, y, y_test, d_train, d_test = get_train_and_test_data(data)
    
    param = {
            'max_depth': 3,
            'eta': 0.3, 
            'silent': 1, 
            'objective': 'multi:softprob',
            'num_class': 2,
            'scale_pos_weight':1}
    
    print ('training model...')
   
    xg_reg = xgb.train(param, d_train, 100)
    
    prob_preds = xg_reg.predict(d_test)
    best_preds = np.asarray([np.argmax(line) for line in prob_preds])

    accuracy = roc_auc_score(y_test, best_preds)
    print("ROC_AUC_SCORE: %.2f%%" % (accuracy * 100.0))
    
    return xg_reg, X, X_with_cep, y_test, prob_preds, best_preds