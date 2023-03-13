import pandas as pd
import model as md
import over_under_sample as ous
import model_analysis
from sklearn.model_selection import StratifiedKFold

def model_selection(train, test):
    # Plots performance of each model with and without upsampling
    modelchoice = ['randomforest', 'xgboost', 'svc', 'lgbm']
    x_train = train.drop(columns='label')
    y_train = train['label']

    cv = StratifiedKFold(n_splits=10, random_state=42, shuffle=True)

    list_score = []
    list_testsetscore = []
    list_score_upsample = []
    list_testsetscore_upsample = []
    for model in modelchoice:
        for train_idx, valid_idx in cv.split(x_train, y_train):
            trainset = pd.concat([x_train.iloc[list(train_idx)], y_train.iloc[list(train_idx)]],axis=1)
            validset = pd.concat([x_train.iloc[list(valid_idx)],y_train.iloc[list(valid_idx)]],axis=1)
            
            validscore = md.callmodel(trainset, model, separatetestset=True, testsetdf=validset, all=True)
            list_score.append(validscore)
            
            testsetscore = md.callmodel(trainset, model, separatetestset=True, testsetdf=test, all=True)
            list_testsetscore.append(testsetscore)
                
        for train_idx, valid_idx in cv.split(x_train, y_train):
            trainset = pd.concat([x_train.iloc[list(train_idx)], y_train.iloc[list(train_idx)]],axis=1)
            validset = pd.concat([x_train.iloc[list(valid_idx)],y_train.iloc[list(valid_idx)]],axis=1)
            trainset = ous.callupsample(trainset)
            
            validscore_upsample = md.callmodel(trainset, model, separatetestset=True, testsetdf=validset, all=True)
            list_score_upsample.append(validscore_upsample)
            
            testsetscore_upsample = md.callmodel(trainset, model, separatetestset=True, testsetdf=test, all=True)
            list_testsetscore_upsample.append(testsetscore_upsample)
        
    output_df = pd.DataFrame({'list_score': list_score, 'list_testsetscore': list_testsetscore, 'list_score_upsample': list_score_upsample, 'list_testsetscore_upsample':list_testsetscore_upsample })
    model_analysis.F1_boxplots_models(output_df)
    