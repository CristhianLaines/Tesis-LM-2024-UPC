from LOGICA.PreProcesarData import *
from SCRIPTS import *

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, f1_score, _classification_report, roc_curve, accuracy_score, precision_score, recall_score, accuracy_score
from xgboost import XGBClassifier
from sklearn.ensemble import StackingClassifier

def regresion_logistica(x, y):
    modelo_logistico = LogisticRegression(solver='liblinear')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=42)

    modelo_logistico.fit(x_train, y_train)

    y_pred_RLog = modelo_logistico.predict(x_test)
    y_pred_RLog_probba = modelo_logistico.predict_proba(x_test)

    print('Regresión Logística')
    confusion_matrix = confusion_matrix(y_test, y_pred_RLog)
    print(classification_report(y_test, y_pred_RLog))
    print(confusion_matrix)
    print(pd.DataFrame(confusion_matrix, columns=['Predicción NO', 'Predicción SI'], index=['Real NO', 'Real SI']))

    print('Accuracy: ', accuracy_score(y_test, y_pred_RLog))
    print('Precision: ', precision_score(y_test, y_pred_RLog))
    print('Recall: ', recall_score(y_test, y_pred_RLog))
    print('F1: ', f1_score(y_test, y_pred_RLog))
    print('AUC: ', roc_auc_score(y_test, y_pred_RLog_probba[:, 1]))

    return

def random_foreset(x, y):
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=42)

    modelo_rf.fit(x_train, y_train)

    y_pred_rf = modelo_rf.predict(x_test)
    y_pred_rf_proba = modelo_rf.predict_proba(x_test)

    print('Random Forest')
    confusion_matrix = confusion_matrix(y_test, y_pred_rf)
    print(classification_report(y_test, y_pred_rf))
    print(confusion_matrix)
    print(pd.DataFrame(confusion_matrix, columns=['Predicción NO', 'Predicción SI'], index=['Real NO', 'Real SI']))

    print('Accuracy: ', accuracy_score(y_test, y_pred_rf))
    print('Precision: ', precision_score(y_test, y_pred_rf))
    print('Recall: ', recall_score(y_test, y_pred_rf))
    print('F1: ', f1_score(y_test, y_pred_rf))
    print('AUC: ', roc_auc_score(y_test, y_pred_rf_proba[:, 1]))

    return

def xg_boost(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=0)

    params = {
        'objectives':'binary:logistic',
        'eval_metric' : 'auc'
    }
    
    modelo_xgb = XGBClassifier(**params)
    
    modelo_xgb.fit(x_train, 
               y_train,
               eval_set=[(x_test, y_test)],
               verbose=True
    )

    y_pred_xgb = modelo_xgb.predict(x_test)
    y_pred_xgb_proba = modelo_xgb.predict_proba(x_test)

    print('XGBoost')
    confusion_matrix = confusion_matrix(y_test, y_pred_xgb)
    print(classification_report(y_test, y_pred_xgb))
    print(confusion_matrix)
    print(pd.DataFrame(confusion_matrix, columns=['Predicción NO', 'Predicción SI'], index=['Real NO', 'Real SI']))

    print('Accuracy: ', accuracy_score(y_test, y_pred_xgb))
    print('Precision: ', precision_score(y_test, y_pred_xgb))
    print('Recall: ', recall_score(y_test, y_pred_xgb))
    print('F1: ', f1_score(y_test, y_pred_xgb))
    print('AUC: ', roc_auc_score(y_test, y_pred_xgb_proba[:, 1]))

    return

def stacking(x, y):

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=42)

    rf = RandomForestClassifier(random_state=42)

    # Definir los modelos base
    rf = RandomForestClassifier()
    xgb = XGBClassifier()
    log_reg = LogisticRegression()

    # Definir los hiperparámetros para cada modelo base
    param_grid_rf = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }

    param_grid_xgb = {
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1],
        'max_depth': [3, 6, 10]
    }

    param_grid_log_reg = {
        'C': [0.1, 1, 10],
        'solver': ['lbfgs', 'liblinear']
    }

    # Realizar la búsqueda de hiperparámetros
    grid_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy')
    grid_xgb = GridSearchCV(xgb, param_grid_xgb, cv=5, scoring='accuracy')
    grid_log_reg = GridSearchCV(log_reg, param_grid_log_reg, cv=5, scoring='accuracy')

    grid_rf.fit(X_train, y_train)
    grid_xgb.fit(X_train, y_train)
    grid_log_reg.fit(X_train, y_train)

    # Obtener los mejores modelos
    best_rf = grid_rf.best_estimator_
    best_xgb = grid_xgb.best_estimator_
    best_log_reg = grid_log_reg.best_estimator_

    # Definir el modelo de stacking
    estimators = [
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('log_reg', best_log_reg)
    ]

    stacking_clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())

    # Entrenar el modelo de stacking
    stacking_clf.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = stacking_clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    return


def modelo(df_final: pd.DataFrame):

    x = df_final.drop('TARGET', axis=1)
    y = df_final['TARGET']

    # Regresión logística
    regresion_logistica(x, y)

    # Random Forest
    random_foreset(x, y)

    # XG Boost
    xg_boost(x, y)

    # Stacking
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.6, random_state=42)

    rf = RandomForestClassifier(random_state=42)

    # Definir los modelos base
    rf = RandomForestClassifier()
    xgb = XGBClassifier()
    log_reg = LogisticRegression()

    # Definir los hiperparámetros para cada modelo base
    param_grid_rf = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }

    param_grid_xgb = {
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1],
        'max_depth': [3, 6, 10]
    }

    param_grid_log_reg = {
        'C': [0.1, 1, 10],
        'solver': ['lbfgs', 'liblinear']
    }

    # Realizar la búsqueda de hiperparámetros
    grid_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='accuracy')
    grid_xgb = GridSearchCV(xgb, param_grid_xgb, cv=5, scoring='accuracy')
    grid_log_reg = GridSearchCV(log_reg, param_grid_log_reg, cv=5, scoring='accuracy')

    grid_rf.fit(X_train, y_train)
    grid_xgb.fit(X_train, y_train)
    grid_log_reg.fit(X_train, y_train)

    # Obtener los mejores modelos
    best_rf = grid_rf.best_estimator_
    best_xgb = grid_xgb.best_estimator_
    best_log_reg = grid_log_reg.best_estimator_

    # Definir el modelo de stacking
    estimators = [
        ('rf', best_rf),
        ('xgb', best_xgb),
        ('log_reg', best_log_reg)
    ]

    stacking_clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())

    # Entrenar el modelo de stacking
    stacking_clf.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = stacking_clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')


    # Predecir
    df_practicantes = read_data(Q_PRACTICANTES_ACTIVOS)

    matricula = input('Ingrese la matrícula del practicante: ')
    matricula = str(matricula).zfill(7)

    df_practicante = df_practicantes[df_practicantes['Matricula'] == matricula]

    df_practicante = df_practicante.drop(['Cod_SIGA', 'Matricula'], axis=1)

    stacking_clf.predict(df_practicante)
    
    return 