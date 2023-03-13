import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def scale(df):
    # Scales using min max scaling
    scaler = MinMaxScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df
