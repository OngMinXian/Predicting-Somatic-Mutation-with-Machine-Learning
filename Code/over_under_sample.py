import pandas as pd
from sklearn.utils import resample

def up_sample(df):
    # separate minority and majority classes
    not_somatic = df[df.label==0]
    somatic = df[df.label==1]

    # upsample minority
    somatic_upsampled = resample(somatic,
                            replace=True, # sample with replacement
                            n_samples=len(not_somatic), # match number in majority class
                            random_state=42) # reproducible results

    # combine majority and upsampled minority
    resampled_data = pd.concat([not_somatic, somatic_upsampled])

    # check new class counts
    # print(resampled_data.label.value_counts())

    return resampled_data

def down_sample(df):
    # separate minority and majority classes
    not_somatic = df[df.label==0]
    somatic = df[df.label==1]

    # upsample minority
    not_somatic_downsampled = resample(not_somatic,
                            replace=False, # sample without replacement
                            n_samples=len(somatic), # match number in minority class
                            random_state=27) # reproducible results

    # combine majority and upsampled minority
    resampled_data = pd.concat([somatic, not_somatic_downsampled])

    # check new class counts
    # print(resampled_data.label.value_counts())

    return resampled_data