# Predicting somatic mutations using Machine Learning based methods 
 
### About the project 
--- 
There exist many variant callers that aims to identify variants which helps in studying mutations that drive tumorigenesis. This project aims to predict somatic mutations using machine learning and the derived information from these callers. 
 
### Data processing 
--- 
From the VCF files, a total of 16 features were parsed. These included: 
| Caller | Feature | Caller | Feature | 
|-----------|--------|-----------|--------| 
| Mutect2    | MQ | Varscan    | SSF | 
|     | MQRankSum |     | MSI | 
|     | TLOD |     | SOR | 
|     | ReadPosRankSum |     | FILTER_Varscan | 
|     | NLOD | Vardict    | SSC | 
|     | FILTER_Mutect2 |    | SPV | 
| Freebayes    | MQM |    | FILTER_Vardict | 
|     | MQMR | | |
|     | FILTER_Freebayes | | |

Notable features that were dropped include: 
* Chromosome and position 
* Reference and alternate nucleotide 

This is because identical mutations in different people might lead to different results. 
 
### Exploratory data analysis 
--- 
<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Class_Distribution.png"> <br />
Class distribution plot implies that the data contains a higher proportion of non-somatic mutation than somatic mutation except syn5 which is the opposite. Imbalanced classification could possibly result in poorer model performance. 
 
<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Boxplots_Feature.png"> <br />
Boxplot shows the distribution between somatic and non-somatic mutations among the features. Notable features that show a very similar distribution (similar median) between somatic and non-somatic mutations include mt2_NLOD, m2_ReadPosRankSum, vd_MSI, vd_SOR. 
 
<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Missing_Data.png"> <br />
Missing data matrix shows that there is a significant amount of missing data found in every feature except the filters. This is due to the possiblility that not all variant callers identify the SNP as a variant. This means that data is not random by chance and was hence converted to additional features (where each feature has a derived feature indicating whether the data is missing). The imputation method chosen to fill in the missing data was median due to the presence of outliers.

<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Anova_Chi-square.png"> <br />
Chi-square and ANOVA test were conducted on the features. All the p-values were less than 0.05 which indicates that each feature is significant between somatic and non-somatic mutations. However, there are some noticeably low effect size: FILTER_Varscan and m2_NLOD. These features are removed to reduce the model's complexity and reduce chance of errors.

<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Correlation_Matrix.png"> <br />
Correlation matrix shows the correlation between features. f_MQMR and m2_MQ are highly correlated. Removing highly correlated feature can reduce the model's complexity and reduce chance of errors. Based on the ANOVA results, f_MQMR will be removed due to its lower effect size.
 
### Model selection 
--- 
<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Boxplots_F1.png"> <br />
 The following models were considered: Random Forest, XGBoost, C-Support Vector Classification, Light Gradient Boosting Model. Stratified 10-fold cross validation was performed on each model using real1 as the training set and real2_part1 as the test set. This was repeated with upsampling of the training set to solve the problem of imbalanced classification. The boxplots shows that random forest without upsampling performed the best.
 
### Adding synthetic data 
--- 
<img src="https://github.com/OngMinXian/Predicting-Somatic-Mutation-with-Machine-Learning/blob/main/Graphs/Adding_Syn_Data_syn1.png"> <br />
 To increase the diversity of data, synthetic data could be added to the training set. Synthetic data 1 to 5 of different amount (0 to 100% in increments of 5%) was added and ran against stratified 20-fold cross validation. Only syn1's plot is shown above but the rest of the plots can be found in the repository. The percentage corresponding to the best test score that did not deviate too far from cross validation score (too different will imply overfitting) was chosen. The results are as follow:
 | Data | Percentage |
 |-----------|--------|
 | syn1    | 0.10 |
 | syn2    | 0.00 |
 | syn3    | 0.05 |
 | syn4    | 0.05 |
 | syn5    | 0.15 |
 
### Model tuning 
--- 
 Lastly, the model's parameters was tuned using a hyperparameter grid and random searching. 100 iterations were ran with 3-fold cross validation. The following parameters were found to improve F1 score from 88.3% to 88.9%.
 | Parameter | Value |
 |-----------|--------|
 | n_estimators    | 100 |
 | min_samples_split    | 2 |
 | min_samples_leaf    | 4 |
 | max_depth    | 30 |
 | bootstrap    | True |
 
### Conclusions 
--- 
 | Metric | Value |
 |-----------|--------|
 | Precision    | 98.9% |
 | Recall    | 80.8& |
 | F1    | 88.9% |
 | AUC_PR    | 90.0% |
 
 The two best variant callers were Mutect2 and Vardict which performed with F1 score of 80.4% and 78.0% respectively across all datasets combined. The intersection of these 2 callers (where 1/0 were treated as 0s) resulted in an F1 score of 81.3%. The model performs better than this naive approach which shows that a machine learning approach with the variant callers might lead to a more effective method instead. However, the model performed an F1 score of 82.8% with real2_part2 which could suggest that there is overfitting. However, this is still marginally better than the expected performance of the intersection of the 2 callers.
 
### Acknowledgements 
---
This project was adapted from a project done with Yusong and Matthias in CS4220.
