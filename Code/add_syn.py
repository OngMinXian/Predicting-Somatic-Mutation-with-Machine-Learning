import numpy as np
import pandas as pd
import model as md
import model_analysis
from sklearn.model_selection import StratifiedKFold

def add_syn(data):
    # Adds different amount of each synthetic data 
    train, test = data['real1'], data['real2_part1']
    for i in ['syn4', 'syn5']:
        print(i)
        df_to_sample = data[i]
        mean_f1_score = []
        mean_test = []

        for frac in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
            print(frac, end=" ")
            sample = df_to_sample.sample(frac=frac, random_state=42)
            dftrain = pd.concat([sample, train], axis=0, ignore_index=True)
            
            x_train = dftrain.drop(columns='label')
            y_train = dftrain['label']

            mean_score = []
            mean_testsetscore = []
            cv = StratifiedKFold(n_splits=20, shuffle=True)
            for train_idx, valid_idx in cv.split(x_train, y_train):
                trainset = pd.concat([x_train.iloc[list(train_idx)], y_train.iloc[list(train_idx)]], axis=1)
                validset = pd.concat([x_train.iloc[list(valid_idx)], y_train.iloc[list(valid_idx)]], axis=1)
                
                score = md.callmodel(trainset, model='randomforest', separatetestset=True, testsetdf=validset, f1=True)
                mean_score.append(score)
                
                testsetscore = md.callmodel(trainset, model='randomforest', separatetestset=True, testsetdf=test, f1=True)
                mean_testsetscore.append(testsetscore)
            
            
            mean_f1_score.append(np.mean(mean_score))
            mean_test.append(np.mean(mean_testsetscore))
        
        output_df = pd.DataFrame({'sample_frac': [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1],'cv_score': mean_f1_score, 'test_score': mean_test })
        model_analysis.F1_add_syn_data(output_df, i)
        print()
