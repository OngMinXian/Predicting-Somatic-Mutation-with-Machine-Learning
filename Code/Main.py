# Import libraries
import pandas as pd
import extract_features
import process_data
import eda
import scaling
import imputation
from model_selection import model_selection
from add_syn import add_syn
from hyperparametric_tuning import hyperparametric_tuning
from model import callmodel

# Extract out addition features from Mutect2, Freebayes and Vardict
for i in ['syn1', 'syn2', 'syn3', 'syn4', 'syn5', 'real1', 'real2_part1']:
    print('Extracting out features for', i)
    extract_features.extractFeatureMT2('Data/' + i + '/' + i + '-mutect2.vcf.gz')
    extract_features.extractFeatureFB('Data/' + i + '/' + i + '-freebayes.vcf.gz')
    extract_features.extractFeatureVD('Data/' + i + '/' + i + '-vardict.vcf.gz')

# Process features
for data in ['syn1', 'syn2', 'syn3', 'syn4', 'syn5', 'real1', 'real2_part1']:
    print('Processing features for', data)
    process_data.process_data('Data/' + data).to_csv('Data/processed/' + data + '_processed.csv', index=False)

# # Exploratory data analysis
print('Exploring data')
data = {}
for i in ['syn1', 'syn2', 'syn3', 'syn4', 'syn5', 'real1', 'real2_part1']:
    data[i] = pd.read_csv('Data/processed/' + i + '_processed.csv')
combined_data = pd.concat([
    data['syn1'],
    data['syn2'],
    data['syn3'],
    data['syn4'],
    data['syn5'],
    data['real1'],
    data['real2_part1'],
], axis=0, ignore_index=True)

eda.count_plot(data)
eda.count_missing_data(combined_data)
eda.correlation_matrix(combined_data)
eda.plot_boxplot(combined_data)
eda.bivstats(combined_data)

# Drops features
print('Dropping features')
for k, v in data.items():
    data[k] = v.drop(columns=['FILTER_Varscan', 'm2_NLOD', 'f_MQMR'])

# Scale data
print('Scale features')
for k, v in data.items():
    data[k] = scaling.scale(v)

# Imputes data
print('Imputes data')
for k, v in data.items():
    data[k] = imputation.Imputer(v, method='median')

# Saves final processed files before training
for k, v in data.items():
    v.to_csv('Data/training_data/' + k + '_train.csv', index=False)

# Model selection
print('Model selection')
model_selection(data['real1'], data['real2_part1'])

# Adds synthetic data to training data
print('Adding synthetic data')
add_syn(data)
training_data = pd.concat(
    [
        data['real1'],
        data['syn1'].sample(frac=0.1, random_state=42),
        data['syn3'].sample(frac=0.05, random_state=42),
        data['syn4'].sample(frac=0.05, random_state=42),
        data['syn5'].sample(frac=0.15, random_state=42)
    ], 
    axis=0)

# Hyperparametric tuning
print('Hyperparametric tuning')
hyperparametric_tuning(training_data)

# Final training with tuned hyperparameters
callmodel(data['real1'], model='randomforest', separatetestset=True, testsetdf=data['real2_part1'], all=True)
callmodel(data['real1'], model='final', separatetestset=True, testsetdf=data['real2_part1'], all=True)
