import argparse
import numpy as np
import pandas as pd

def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

def preprocess(df, inference=False):
    # result = pd.DataFrame()
    # result = pd.concat([result, pd.get_dummies(df['University'], drop_first=True)],axis=1)
    # result = pd.concat([result, pd.get_dummies(df['Degree'], drop_first=True)],axis=1)
    # if inference == False:
    #     result = pd.concat([result, df[['Rating']]],axis=1)
    # return result
    pass

def save_data(data_path, df):
    df.to_csv(data_path.replace('.csv','_processed.csv'), index=False)
    return None

def run(data_path):
    df = load_data(data_path)
    # df = preprocess(df)
    save_data(data_path, df)
    return df

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    args = argparser.parse_args()
    run(args.data_path)