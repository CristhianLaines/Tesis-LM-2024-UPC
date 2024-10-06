from LOGICA.Modelo import *

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

def evaluar(df: pd.DataFrame):

    return