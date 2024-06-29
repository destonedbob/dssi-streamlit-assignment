import argparse
import logging

from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import preprocess
import model_registry

logging.basicConfig(level=logging.INFO)

features = ['NUS', 'NUS-ISS', 'SMU', 'Accountancy and Business',
       'Aerospace Engineering', 'Art, Design and Media',
       'Artificial Intelligence Systems', 'Arts', 'Arts (Architecture)',
       'Arts (Industrial Design)', 'Arts and Education', 'Bioengineering',
       'Biological and Biomedical Sciences',
       'Biomedical Sciences and Chinese Medicine', 'Business',
       'Business Administration', 'Business Administration (Accountancy)',
       'Business Management', 'Business and Computer Engineering/Computing',
       'Chemical and Biomolecular Engineering',
       'Chemistry and Biological Chemistry', 'Chinese', 'Civil Engineering',
       'Communication Studies', 'Computer Engineering', 'Computer Science',
       'Computing (Computer Science)', 'Computing (Information Security)',
       'Computing (Information Systems)',
       'Data Science and Artificial Intelligence', 'Dental Surgery',
       'Digital Leadership', 'Economics',
       'Electrical and Electronic Engineering',
       'Engineering (Biomedical Engineering)',
       'Engineering (Chemical Engineering)', 'Engineering (Civil Engineering)',
       'Engineering (Computer Engineering)',
       'Engineering (Electrical Engineering)',
       'Engineering (Engineering Science)',
       'Engineering (Environmental Engineering)',
       'Engineering (Industrial and Systems Engineering)',
       'Engineering (Materials Science and Engineering)',
       'Engineering (Mechanical Engineering)', 'Engineering and Economics',
       'English', 'Enterprise Business Analytics',
       'Environmental Earth Systems Science', 'Environmental Engineering',
       'Environmental Studies', 'History', 'Information Engineering and Media',
       'Information Systems', 'Interdisciplinary Double Major',
       'Landscape Architecture', 'Law', 'Linguistics and Multilingual Studies',
       'Maritime Studies', 'Materials Engineering',
       'Mathematics and Mathematical Sciences', 'Mechanical Engineering',
       'Medicine', 'Medicine and Surgery', 'Music', 'Philosophy',
       'Physics and Applied Physics', 'Psychology',
       'Public Policy and Global Affairs', 'Science',
       'Science (Business Analytics)', 'Science (Computational Biology)',
       'Science (Data Science and Analytics)', 'Science (Nursing)',
       'Science (Pharmaceutical Science)', 'Science (Pharmacy)',
       'Science (Project and Facilities Management)', 'Science (Real Estate)',
       'Science and Education', 'Social Sciences', 'Sociology',
       'Software Engineering', 'Sports Science and Management']
label = 'Rating'

def run(data_path, model_path, f1_criteria):
    logging.info('Process Data...')
    df = preprocess.run(data_path)
    
    #Train-Test Split
    logging.info('Start Train-Test Split...')
    X_train, X_test, y_train, y_test = train_test_split(df[features], \
                                                        df[label], \
                                                        test_size=0.2, \
                                                        random_state=0)
    
    #Train Classifier
    logging.info('Start Training...')
    random_forest = RandomForestClassifier(n_estimators=10,
                                           max_depth=4, 
                                           class_weight = "balanced",
                                           n_jobs=2)
    
    random_forest.fit(X_train, y_train)
    
    #Evaluate and Deploy
    logging.info('Evaluate...')
    score = f1_score(y_test, random_forest.predict(X_test), average='weighted')
    if score >= f1_criteria:
        logging.info('Deploy...')
        mdl_meta = { 'name': 'loan_approval', 'metrics': f"f1:{score}" }
        model_registry.register(random_forest, features, mdl_meta)
        #dump(clf, model_path+'mdl.joblib')
        #dump(features, model_path+'raw_features.joblib')
    
    logging.info('Training completed.')
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    argparser.add_argument("--model_path", type=str)
    argparser.add_argument("--f1_criteria", type=float)
    args = argparser.parse_args()
    run(args.data_path, args.model_path, args.f1_criteria)