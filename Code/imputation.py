import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

def Imputer(df, method=None, constant=np.nan, columns=None):
    # Imputes missing data using given method
    # If method is empty, list out all available methods to impute

    # No method given
    if method == None:
        print("Available methods:\n- mean\n- median\n- most_frequent\n- constant\n- linear_regression\n- kNN \n- missing_as_feature")
        return df

    else:

        df = df.copy()

        # Checks if label is inside df and saves it to concat at the end
        if 'label' in df.columns:
            label = df[['label']]
            df = df.drop(columns=['label'])
            have_label = True
        else:
            have_label = False

        if 'Chr' in df.columns:
            Chr = df[['Chr']]
            df = df.drop(columns=['Chr'])
            start = df[['START_POS_REF']]
            df = df.drop(columns=['START_POS_REF'])
            have = True
        else:
            have = False

        # If no columns given, apply to all columns
        if not columns:
            columns = df.columns

        # Fills NA with mean
        if method == 'mean':
            imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
            imputer.fit(df[columns])
            df[columns] = imputer.transform(df[columns])
        
        # Fills NA with median
        if method == 'median':
            imputer = SimpleImputer(missing_values=np.nan, strategy='median')
            imputer.fit(df[columns])
            df[columns] = imputer.transform(df[columns])
        
        # Fills NA with most frequent value
        if method == 'most_frequent':
            imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
            imputer.fit(df[columns])
            df[columns] = imputer.transform(df[columns])
        
        # Fills NA with constant
        if method == 'constant':
            imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=constant)
            imputer.fit(df[columns])
            df[columns] = imputer.transform(df[columns])
        
        # Fills NA using a linear regression model
        if method == 'linear_regression':
            for column in columns:
                # Imputes other columns using a simpler imputation method first and splits into train, to_predict
                df_copy = df.copy()
                df_copy = Imputer(df_copy, method='median', columns=list(df_copy.columns.drop([column])))
                train, to_predict = df_copy[~df_copy[column].isna()], df_copy[df_copy[column].isna()].drop(columns=[column])
                if to_predict.empty:
                    continue
                x, y = train.drop(columns=[column]), train[column]
                # Fit model and predict
                lr_model = LinearRegression()
                lr_model.fit(x, y)
                df[column][df[column].isna()] = lr_model.predict(to_predict)

        if method == 'missing_as_feature':
            new_cols = pd.DataFrame()
            for column in columns:
                if sum(df[column].isna()) == 0:
                    continue
                new_col = pd.DataFrame({column + '_missing':((~df[column].isna()).apply(lambda x: 0 if x else 1))})
                new_cols = pd.concat([new_cols, new_col], axis=1)
            df = pd.concat([df, new_cols], axis=1)
        
        if have:
            return pd.concat([df, Chr, start], axis=1)
        else:
            return pd.concat([df, label], axis=1) if have_label else df
