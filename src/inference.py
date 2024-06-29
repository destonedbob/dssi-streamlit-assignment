import pandas as pd
import numpy as np
from .model_registry import retrieve

model_name = 'uni_rating'

def get_prediction(**kwargs):
    clf, features = retrieve(model_name)
    pred_df = pd.DataFrame(kwargs, index=[0])
    pred = clf.predict(pred_df[features])
    pred = np.round(pred).astype(int)
    return pred[0]
