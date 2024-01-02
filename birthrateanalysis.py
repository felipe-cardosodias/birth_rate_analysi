import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

def fileread(readdatabase):
    births = pd.read_csv(readdatabase) 
    births['day'].fillna(0, inplace=True) 
    births['day'] = births['day'].astype(int)
    births['decade'] = 10 * (births['year'] // 10)
    births.pivot_table('births', 
                        index='decade', 
                        columns='gender', 
                        aggfunc='sum')
    return births

def dataprocessing(processingdatabase):
    births_dpb = fileread(processingdatabase)
    sns.set()
    quartiles = np.percentile(births_dpb['births'], [25,50, 75])
    mu = quartiles[1]
    sig = 0.74 * (quartiles[2] - quartiles[0])
    births_dpb = births_dpb.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
    births_dpb['day'] = births_dpb['day'].astype(int)
    births_dpb.index = pd.to_datetime(10000*births_dpb.year + 100 * births_dpb.month + births_dpb.day, format='%Y%m%d')
    births_dpb['dayofweek'] = births_dpb.index.dayofweek    
    return births_dpb
    
def results(database):
    results_database = dataprocessing(database)
    births_month = results_database.pivot_table('births', 
                                                [results_database.index.month, 
                                                results_database.index.day])
    births_month.index = [pd.datetime(2012, month, day)
                        for (month, day) in births_month.index]
    fig, ax = plt.subplots(figsize=(12,4))
    births_month.plot(ax=ax)
    plt.show()    

if __name__ == "__main__":
    results("births.csv")
