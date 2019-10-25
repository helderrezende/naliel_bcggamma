import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import shap
import numpy as np

from datalayer import read_sia_model


def get_train_and_test_data(path, method):
    data = read_sia_model(path, method)
    data = data.dropna(subset=['AR_ESTADI'])
    
    X = data[['AP_TIPPRE', 'AP_NUIDADE', 'AP_RACACOR', 'AP_SEXO', 'AP_CEPPCN_REGIAO', 'AP_CEPPCN_SUBREGIAO',
              'AP_CEPPCN_SETOR', 'AP_CEPPCN_SUBSETOR', 'AP_CEPPCN_DIVISOR_SUBSETOR',
              'AP_CEPPCN_SUFIXO_DISTRIBUICAO', 'AP_MUNPCN_LATITUDE', 'AP_MUNPCN_LONGITUDE',
              'AP_MUNPCN_CAPITAL', 'AP_MUNPCN_CODIGO_UF', 'AP_UFMUN_LATITUDE',
              'AP_UFMUN_LONGITUDE', 'AP_UFMUN_CAPITAL', 'AP_UFMUN_CODIGO_UF',
              'CLINICAS_AMB_ESPECIALIZADO', 'HOSPITAL_ESPECIALIZADO', 'HOSPITAL_GERAL', 
              'UN_BASICA_SAUDE', 'UN_DIAG_TERAPIA', 'LEITOS_INTERNACAO', 'MAMOGRAFOS',
              'RAIO_X', 'TOMAGRAFOS', 'RESSONANCIA_MAGNETICA',
              'AP_MUNPCN_GINI', 'AP_MUNPCN_RDPC', 'AP_MUNPCN_T_AGUA',
              'AP_MUNPCN_T_BANAGUA', 'AP_MUNPCN_T_LIXO', 'AP_MUNPCN_I_ESCOLARIDADE',
              'AP_MUNPCN_I_FREQ_PROP', 'AP_MUNPCN_IDHM', 'AP_MUNPCN_IDHM_E', 
              'AP_MUNPCN_IDHM_L', 'AP_MUNPCN_IDHM_R', 'MEDICOS', 'ENFERMEIROS']]

    y = data['AR_ESTADI']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    
    d_train = xgb.DMatrix(X_train, label=y_train)
    d_test = xgb.DMatrix(X_test, label=y_test)
    
    return X, y, y_test, d_train, d_test


def get_relevant_features(model, X):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    #shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])
    
    #shap.summary_plot(shap_values, X, plot_type="bar")

def predict_sia(path):
    X, y, y_test, d_train, d_test = get_train_and_test_data(path)
    
    param = {
            'max_depth': 3,
            'eta': 0.3, 
            'silent': 1, 
            'objective': 'multi:softprob',
            'num_class': 5}
   
    xg_reg = xgb.train(param, d_train, 100)
    
    preds = xg_reg.predict(d_test)
    best_preds = np.asarray([np.argmax(line) for line in preds])

    accuracy = accuracy_score(y_test, best_preds)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    
    features = get_relevant_features(xg_reg, X)
    
    return xg_reg
    
if __name__ == '__main__':
    predict_sia()