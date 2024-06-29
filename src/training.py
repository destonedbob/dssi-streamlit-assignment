import argparse
import logging

from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import preprocess
import model_registry

logging.basicConfig(level=logging.INFO)

label = 'Rating'
model_name = 'uni_rating'

def run(data_path, model_path, r2_criteria):
    logging.info('Process Data...')
    df = preprocess.run(data_path)
    features = [col for col in df.columns if col != label]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore")
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, features),
        ]
    )

    #Train-Test Split
    logging.info('Start Train-Test Split...')
    X_train, X_test, y_train, y_test = train_test_split(df[features], \
                                                        df[label], \
                                                        test_size=0.2, \
                                                        random_state=0)
    
    #Train Classifier
    logging.info('Start Training...')
    random_forest = RandomForestRegressor(n_estimators=10,
                                           max_depth=4, 
                                           n_jobs=2)
    
    clf = Pipeline(steps=[("preprocessor", preprocessor),\
                          ("binary_classifier", random_forest)
                         ])
    clf.fit(X_train, y_train)
    
    #Evaluate and Deploy
    logging.info('Evaluate...')
    score = r2_score(y_test, clf.predict(X_test))
    if score >= r2_criteria:
        logging.info('Deploy...')
        mdl_meta = { 'name': model_name, 'metrics': f"R2:{score}" }
        model_registry.register(clf, features, mdl_meta)
        #dump(clf, model_path+'mdl.joblib')
        #dump(features, model_path+'raw_features.joblib')
    
    logging.info('Training completed.')
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    argparser.add_argument("--model_path", type=str)
    argparser.add_argument("--r2_criteria", type=float)
    args = argparser.parse_args()
    run(args.data_path, args.model_path, args.r2_criteria)