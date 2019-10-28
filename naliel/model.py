import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import shap
import numpy as np
import pandas as pd

from datalayer import read_sia_model


def get_train_and_test_data(path, method):
    data = read_sia_model(path, method)
    data['AR_ESTADI'] = data['AR_ESTADI'].apply(pd.to_numeric, errors='coerce')
    data = data.dropna(subset=['AR_ESTADI'])
    
    data['AR_ESTADI'] = np.where(data['AR_ESTADI'] <= 2, 0, 1)
    # AP_TIPPRE
    X_with_cep = data[['AP_CEPPCN',
              'CLINICAS_AMB_ESPECIALIZADO', 'HOSPITAL_ESPECIALIZADO', 'HOSPITAL_GERAL', 
              'UN_BASICA_SAUDE', 'UN_DIAG_TERAPIA', 'LEITOS_INTERNACAO', 'MAMOGRAFOS',
              'RAIO_X', 'TOMAGRAFOS', 'RESSONANCIA_MAGNETICA',
              'AP_MUNPCN_GINI', 'AP_MUNPCN_RDPC', 'AP_MUNPCN_T_AGUA',
              'AP_MUNPCN_AGUA_ESGOTO',
              'AP_MUNPCN_T_BANAGUA', 'AP_MUNPCN_T_LIXO', 'AP_MUNPCN_I_ESCOLARIDADE',
              'AP_MUNPCN_I_FREQ_PROP', 'AP_MUNPCN_IDHM', 'AP_MUNPCN_IDHM_E', 
              'AP_MUNPCN_IDHM_L', 'AP_MUNPCN_T_SLUZ',
              'AP_CODUNI_NOTA',
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
    
    X = X_with_cep.drop('AP_CEPPCN', 1)

    y = data['AR_ESTADI']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    
    d_train = xgb.DMatrix(X_train, label=y_train)
    d_test = xgb.DMatrix(X_test, label=y_test)
    
    return X, X_with_cep, y, y_test, d_train, d_test


def get_relevant_features(model, X):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    #shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])
    
    #shap.summary_plot(shap_values, X, plot_type="bar")

def predict_sia(path, method):
    X, X_with_cep, y, y_test, d_train, d_test = get_train_and_test_data(path, method)
    
    param = {
            'max_depth': 3,
            'eta': 0.3, 
            'silent': 1, 
            'objective': 'multi:softprob',
            'num_class': 2}
   
    xg_reg = xgb.train(param, d_train, 100)
    
    preds = xg_reg.predict(d_test)
    best_preds = np.asarray([np.argmax(line) for line in preds])

    accuracy = accuracy_score(y_test, best_preds)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    
    return xg_reg, X, X_with_cep
    
if __name__ == '__main__':
    data = predict_sia('data/Linfomas Radioterapia SIA-SUS.csv', method='radioterapia')
    print ('Done.')