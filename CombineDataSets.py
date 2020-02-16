import pandas as pd 

cityMetrics = pd.read_csv(r'cleanedCityData.csv')
merchantData = pd. read_csv(r'merchantData.csv')


#cityMetrics.set_index('key').join(merchantData.set_index('key'))
dataSet = pd.merge(cityMetrics, merchantData, on=['City', 'State'])


dataSet.to_csv("finalData.csv", index = False, encoding = 'utf8')