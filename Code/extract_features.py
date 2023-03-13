import parse_features as pf
import pandas as pd

def extractFeatureMT2(filename):
    # extract features out of mutect2 VCF and writes it into a csv file  
    columnName = ['CHROM', 'POS','FILTER', 'MQ', 'MQRankSum', 'TLOD', 'NLOD', 'ReadPosRankSum']
    df = pd.DataFrame(columns=columnName)

    chrom = []
    pos = []
    filter = []
    mq = []
    mqranksum = []
    tlod = []
    nlod = []
    readposranksum = []
    
    for data in pf.lines(filename):
        chrom.append(data.get('CHROM', None))
        pos.append(data.get('POS', None))
        filter.append(data.get('FILTER', None))
        mq.append(data.get('MQ', None))
        mqranksum.append(data.get('MQRankSum', None))
        tlod.append(data.get('TLOD', None))
        nlod.append(data.get('NLOD', None))
        readposranksum.append(data.get('ReadPosRankSum', None))
            
    df = pd.DataFrame(list(zip(chrom, pos, filter, mq, mqranksum, tlod, nlod, readposranksum)),columns =columnName)

    outputName = filename.split("/")[0] + "_MT2_extra_features.csv"
    df.to_csv(outputName, index=False)
    
    return(df)


def extractFeatureFB(filename):
    # extract features out of freebayes VCF and writes it into a csv file
    columnName = ['CHROM', 'POS','FILTER', 'MQM', 'MQMR']
    df = pd.DataFrame(columns=columnName)

    chrom = []
    pos = []
    filter = []
    mqm = []
    mqmr = []
    
    for data in pf.lines(filename):
        chrom.append(data.get('CHROM', None))
        pos.append(data.get('POS', None))
        filter.append(data.get('FILTER', None))
        mqm.append(data.get('MQM', None))
        mqmr.append(data.get('MQMR', None))
        
    df = pd.DataFrame(list(zip(chrom, pos, filter, mqm, mqmr)),columns =columnName)

    outputName = filename.split("/")[0] + "_FB_extra_features.csv"
    df.to_csv(outputName, index=False)
    
    return(df)


def extractFeatureVD(filename):
    # extract features out of vardict VCF and writes it into a csv file
    columnName = ['CHROM', 'POS','FILTER', 'SSF', 'SOR']
    df = pd.DataFrame(columns=columnName)

    chrom = []
    pos = []
    filter = []
    ssf = []
    sor = []
    
    for data in pf.lines(filename):
        chrom.append(data.get('CHROM', None))
        pos.append(data.get('POS', None))
        filter.append(data.get('FILTER', None))
        ssf.append(data.get('SSF', None))
        sor.append(data.get('SOR', None))
        
    df = pd.DataFrame(list(zip(chrom, pos, filter, ssf, sor)),columns =columnName)

    outputName = filename.split("/")[0] + "_VD_extra_features.csv"
    df.to_csv(outputName, index=False)
    
    return(df)
