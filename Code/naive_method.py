# Import libraries
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

# Reads data into pandas dataframe
syn1 = pd.read_csv('Data/processed/syn1_processed.csv')
syn2 = pd.read_csv('Data/processed/syn2_processed.csv')
syn3 = pd.read_csv('Data/processed/syn3_processed.csv')
syn4 = pd.read_csv('Data/processed/syn4_processed.csv')
syn5 = pd.read_csv('Data/processed/syn5_processed.csv')
real1 = pd.read_csv('Data/processed/real1_processed.csv')
real2_part1 = pd.read_csv('Data/processed/real2_part1_processed.csv')
combined_all = pd.concat([syn1, syn2, syn3, syn4, syn5, real1, real2_part1], axis=0)
data = {'syn1':syn1, 'syn2':syn2, 'syn3':syn3, 'syn4':syn4, 'syn5':syn5, 'real1':real1, 'real2_part1':real2_part1}

def statistics(y_test, y_pred):
    # Generates statistics based on test and pred

    #Accuracy
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # #F1_score
    print("f1_score:", f1_score(y_test, y_pred))

    return f1_score(y_test, y_pred)

def naive_estimate(df, col):
    return statistics(df[col], df['label'])

def second_max(lst):
    return sorted(lst)[-2]

# Finds the two best methods
scores = []
for filter in 'FILTER_Mutect2', 'FILTER_Freebayes', 'FILTER_Vardict', 'FILTER_Varscan':
        print("===== Data:", 'combined_all', 'Method:', filter.split('_')[1], '=====')
        score = naive_estimate(combined_all, filter)
        scores.append(score)

combined_all_best_filter = ['FILTER_Mutect2', 'FILTER_Freebayes', 'FILTER_Vardict', 'FILTER_Varscan'][scores.index(max(scores))]
combined_all_second_best_filter = ['FILTER_Mutect2', 'FILTER_Freebayes', 'FILTER_Vardict', 'FILTER_Varscan'][scores.index(second_max(scores))]


print('\n============================================')
print('Top 2 filters')
print('============================================')
print('best filter:', combined_all_best_filter.split('_')[1])
print('2nd best filter:', combined_all_second_best_filter.split('_')[1])
print('\n')

# Uses the intersect of the two best methods
def intersect(method1, method2, label):
    # treats 0/1 and 1/0 as 0
    print('=== intersection of top 2 methods ===')
    index = method1 != method2
    method1[index] = 0
    statistics(method1, label)

for k, v in data.items():
    print(k)
    combined_all = v
    mt2 = combined_all.copy()['FILTER_Mutect2']
    vd = combined_all.copy()['FILTER_Vardict']
    label = combined_all.copy()['label']

    # mt2 intersect with vd
    intersect(mt2, vd, label)
