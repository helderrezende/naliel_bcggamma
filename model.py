import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from datalayer import read_csv_sia

def predict_sia(path):
    path = '../data/Linfomas Radioterapia SIA-SUS.csv'
    data = read_csv_sia(path, 'radioterapia')
    data = data.dropna(subset=['AR_ESTADI'])
    
    X = data[['AP_TIPPRE', 'AP_NUIDADE', 'AP_CEPPCN_REGIAO', 'AP_CEPPCN_SUBREGIAO',
              'AP_CEPPCN_SETOR', 'AP_CEPPCN_SUBSETOR', 'AP_CEPPCN_DIVISOR_SUBSETOR',
              'AP_CEPPCN_SUFIXO_DISTRIBUICAO', 'AP_MUNPCN_latitude', 'AP_MUNPCN_longitude',
              'AP_MUNPCN_capital', 'AP_MUNPCN_codigo_uf', 'AP_UFMUN_latitude',
              'AP_UFMUN_longitude', 'AP_UFMUN_capital', 'AP_UFMUN_codigo_uf']]

    y = data['AR_ESTADI']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    
    xg_reg = xgb.XGBClassifier()
    
    xg_reg.fit(X_train,y_train)
    
    # make predictions for test data
    preds = xg_reg.predict(X_test)
    
    accuracy = accuracy_score(y_test, preds)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    
if __name__ == '__main__':
    predict_sia()