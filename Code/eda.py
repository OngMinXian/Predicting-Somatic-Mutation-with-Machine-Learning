import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno
import scipy
import dataframe_image as dfi

def count_plot(data):
    # Counts the number of 1/0 labels in each data set
    for k, v in data.items():
        v['Dataset'] = k
    df = pd.concat([
            data['syn1'],
            data['syn2'],
            data['syn3'],
            data['syn4'],
            data['syn5'],
            data['real1'],
            data['real2_part1'],
        ], axis=0, ignore_index=True)
    sns.countplot(data=df, x='Dataset', hue='label')
    plt.title('Class Distributions \n (0: Not Somatic Mutation || 1: Somatic Mutation)')
    plt.xlabel('Dataset')
    plt.ylabel('Count')
    plt.savefig('Graphs/Class_Distribution.png', bbox_inches='tight', dpi=200)
    for k, v in data.items():
        v.drop(columns=['Dataset'], inplace=True)
    plt.clf()

def count_missing_data(df):
    # Plots a matrix of missing data
    mat = missingno.matrix(df.drop(columns=['label']).sample(n=5000))
    plt.savefig('Graphs/Missing_Data.png', bbox_inches='tight', dpi=200)
    plt.clf()

def correlation_matrix(df):
    # Plots pearson's correlation matrix
    sns.heatmap(df.corr(), cmap='coolwarm_r', annot=False)
    plt.title('Correlation Matrix')
    plt.savefig('Graphs/Correlation_Matrix.png', bbox_inches='tight', dpi=200)
    plt.clf()

def plot_boxplot(df):
    # Plots boxplot to see distribution of each feature
    figure, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7), (ax8, ax9, ax10, ax11)) = plt.subplots(3, 4)
    axes = ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7), (ax8, ax9, ax10, ax11))
    features = list(df.columns)
    for i in range(3):
        for j in range(4):
            sns.boxplot(x='label', y=features[i * 4 + j], data=df, showfliers=False, ax=axes[i][j], notch=False)
    plt.savefig('Graphs/Boxplots.png', dpi=200)
    plt.clf()

def bivstats(df):
    # Conducts anova/F-test or chi-square test depending on whether feature is continous or discrete
    def anova(df, feature, label):
        # Conducts anova test
        groups = df[label].unique()
        df_grouped = df.groupby(label)
        group_labels = []
        for g in groups:
            g_list = df_grouped.get_group(g)
            group_labels.append(g_list[feature])
        return scipy.stats.f_oneway(*group_labels)
    label = 'label'
    output_df = pd.DataFrame(columns= ["Stat", "+/-", "Effect size", "p-value"])
    for col in df:
        if not col == label:
            if 'FILTER' not in col:
                F, p = anova(df[[col, label]].dropna(), col, label)
                str_p = str(round(p, 6)) if round(p, 6) != 0.0 else '<0.01'
                output_df.loc[col] = ["F", "", round(F,3), str_p]
            else:  
                temp = scipy.stats.chi2_contingency(pd.crosstab(df[[col,label]].dropna()[col],df[[col,label]].dropna()[label]))
                str_p = str(round(p, 6)) if round(p, 6) != 0.0 else '<0.01'
                output_df.loc[col] = ["chi2", "", round(temp[0],3), str_p]
    dfi.export(output_df.sort_values(by=["Stat","Effect size"], ascending=[False, False]), 'Graphs/Anova_Chi-square.png')
    