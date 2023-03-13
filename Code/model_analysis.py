# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plot F1 score of cross-validation and test against % of synthetic data added to training data
def F1_add_syn_data(df, name):
    plt.plot(df['sample_frac'], df['test_score'], label='test score')
    plt.plot(df['sample_frac'], df['cv_score'], label='validation score')
    plt.legend()
    plt.xlabel('Percentage of all synthetic data added to real1 for training')
    plt.ylabel('F1 Score')
    plt.title(name)
    plt.savefig('Graphs/Adding_Syn_Data_' + name + '.png', bbox_inches='tight', dpi=200)
    plt.clf()

# Plots boxplots of F1 scores of each method with cv/test/oversampling_cv/oversampling_test
def F1_boxplots_models(df):
    models = ['rf', 'xgb', 'svc', 'lgbm']
    types = ['cv', 'test', 'oversampling cv', 'oversampling test']
    results = pd.DataFrame(columns=['method', 'types', 'f1'])
    for i in range(4):
        for data in df[i*10:(i+1)*10].values:
            cv, test, up_cv, up_test = data

            cv_f1 = float(cv.split(',')[5].strip())
            row = pd.DataFrame([[models[i], types[0], cv_f1]], columns=['method', 'types', 'f1'])
            results = pd.concat([results, row], axis=0)

            test_f1 = float(test.split(',')[5].strip())
            row = pd.DataFrame([[models[i], types[1], test_f1]], columns=['method', 'types', 'f1'])
            results = pd.concat([results, row], axis=0)

            up_cv_f1 = float(up_cv.split(',')[5].strip())
            row = pd.DataFrame([[models[i], types[2], up_cv_f1]], columns=['method', 'types', 'f1'])
            results = pd.concat([results, row], axis=0)

            up_test_f1 = float(up_test.split(',')[5].strip())
            row = pd.DataFrame([[models[i], types[3], up_test_f1]], columns=['method', 'types', 'f1'])
            results = pd.concat([results, row], axis=0)
    results = results[results['method'] != 'gb']
    results = results[results['method'] != 'adaboost']
    sns.boxplot(x='method', y='f1', hue='types', data=results, showfliers=True, notch=False)
    plt.ylim(80, 95)
    plt.savefig('Graphs/Model_Selection.png', bbox_inches='tight', dpi=200)
    plt.clf()
