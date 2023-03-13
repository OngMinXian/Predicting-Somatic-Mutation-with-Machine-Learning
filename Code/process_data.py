# Import libraries
import os
import numpy as np
import pandas as pd

def process_data(directory):
    # Takes in a snv parse text file and a bed file and processes the data
    # Returns a tuple containing the features and label

    # Finds all relevant files in input directory
    bed_filename = False
    for file in os.listdir(directory):
        if 'parse' in file:
            snv_parse_filename = directory + '/' + file
        if 'bed' in file:
            bed_filename = directory + '/' + file
        if 'MT2_extra_features' in file:
            MT2_extra_features_filename = directory + '/' + file
        if 'FB_extra_features' in file:
            FB_extra_features_filename = directory + '/' + file
        if 'VD_extra_features' in file:
            VD_extra_features_filename = directory + '/' + file

    # Reads snv parse text file and bed file into a pandas dataframe
    snv_data = pd.read_csv(snv_parse_filename, delimiter="\t", dtype={"Chr": str})
    if bed_filename != False:
        bed_data = pd.read_csv(bed_filename, delimiter="\t", names=['Chr', 'Start', 'End'])
        # Adds bed results into snv_data 
        # snvs from bed not found inside snv_data are discarded
        bed_dict = {}
        for data in bed_data.values:
            bed_dict[(str(data[0]), data[1])] = True
        label = []
        label_append = label.append
        for data in snv_data.values:
            if (data[0], data[1]) in bed_dict:
                label_append(1)
            else:
                label_append(0)
        snv_data['label'] = label

    # Reads all extra feature files into pandas dataframes and drop features already given
    MT2_extra_features = pd.read_csv(MT2_extra_features_filename, dtype={'CHROM': 'str'})
    MT2_extra_features = MT2_extra_features.drop(columns=['FILTER', 'MQ'])

    FB_extra_features = pd.read_csv(FB_extra_features_filename, dtype={'CHROM': 'str'})
    FB_extra_features = FB_extra_features.drop(columns=['FILTER', 'MQMR'])

    VD_extra_features = pd.read_csv(VD_extra_features_filename, dtype={'CHROM': 'str'})
    VD_extra_features = VD_extra_features.drop(columns=['FILTER', 'SSF'])

    # Combine snv dataframe with extra features
    for extra in [MT2_extra_features, FB_extra_features, VD_extra_features]:
        snv_data = snv_data.merge(extra, how='left', left_on=['Chr', 'START_POS_REF'], right_on=['CHROM', 'POS'])
        snv_data = snv_data.drop(columns=['CHROM', 'POS'])

    # Handles SOR infinite values with max value of SOR + 1
    highest = np.nanmax(snv_data['SOR'][snv_data['SOR'] != np.inf])
    snv_data['SOR'].replace(np.inf, highest + 1, inplace=True)

    # Converts features with True/False to 1/0
    for col in ['FILTER_Mutect2', 'FILTER_Freebayes', 'FILTER_Vardict', 'FILTER_Varscan']:
        snv_data[col] = snv_data[col].apply(lambda x: 1 if x else 0)
    
    # Drops not needed features
    snv_data = snv_data.drop(columns=['END_POS_REF', 'REF', 'ALT', 'REF_MFVdVs', 'ALT_MFVdVs','Sample_Name'])
    
    # Remove duplicates
    snv_data.drop_duplicates(inplace=True)

    # Merge rows with the same Chr and position
    dupes = {}
    for val in snv_data.values:
        dupes[(val[0], val[1])] = dupes.get((val[0], val[1]), 0) + 1
    
    for k, v in dupes.items():
        if v > 1:
            dupes_ = []
            for val in snv_data.values:
                if k == (val[0], val[1]):
                    dupes_.append(val)
            merged = []
            for j in range(len(dupes_[0])):
                chosen_val = pd.NA
                for dup in dupes_:
                    if not pd.isnull(dup[j]):
                        chosen_val = dup[j]
                merged.append(chosen_val)
            for d in dupes_:
                snv_data = snv_data[~((snv_data['Chr'] == d[0]) & (snv_data['START_POS_REF'] == d[1]))]
            snv_data = pd.concat([snv_data, pd.DataFrame([merged], columns=snv_data.columns)]) 
    snv_data = snv_data.drop(columns=['Chr', 'START_POS_REF'])

    # Rename and reorder features
    features_d = {
                'm2_MQ':'m2_MQ', 'MQRankSum':'m2_MQRankSum', 'TLOD':'m2_TLOD', 'NLOD':'m2_NLOD', 'ReadPosRankSum':'m2_ReadPosRankSum',
                'f_MQMR':'f_MQMR', 'MQM':'f_MQM',
                'vs_SSC':'vs_SSC', 'vs_SPV':'vs_SPV',
                'vd_SSF':'vd_SSF', 'vd_MSI':'vd_MSI', 'SOR':'vd_SOR',
                'FILTER_Mutect2':'FILTER_Mutect2', 'FILTER_Freebayes':'FILTER_Freebayes', 'FILTER_Vardict':'FILTER_Vardict', 'FILTER_Varscan':'FILTER_Varscan'
                }
    features = ['m2_MQ', 'm2_MQRankSum', 'm2_TLOD', 'm2_NLOD', 'm2_ReadPosRankSum', 'f_MQMR', 'f_MQM', 'vs_SSC', 'vs_SPV', 'vd_SSF', 'vd_MSI', 'vd_SOR', 'FILTER_Mutect2', 'FILTER_Freebayes', 'FILTER_Vardict', 'FILTER_Varscan']
    if label:
        features_d['label'] = 'label'
        features.append('label')
    snv_data.rename(inplace=True, columns=features_d)
    snv_data = snv_data[features]

    return snv_data
