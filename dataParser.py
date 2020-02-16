import pandas as pd 

data = pd.read_csv(r'cityData.csv')

data = data.drop("Unnamed: 0", axis =1)

data = data.rename(columns={"state": "State"})
data['State'] = data['State'].str.lower()


data = data.rename(columns={"cityPopulation": "City Population"})
data['City Population'] = data['City Population'].map(lambda x: str(x)[str(x).find(":")+1:str(x).find("(")])

data = data.rename(columns={"city": "City"})
data['City'] = data['City'].str.lower()
data['City'] = data['City'].replace('-', ' ', regex=True)
data['City'] = data['City'].map(lambda x: x[:x.rfind(' ')])


new = data['populationBySex'].str.split(")", n=1, expand = True)
data['Female Population'] = new[1]
data['Male Population'] = new[0]
data['Female Population'] = data['Female Population'].map(lambda x: str(x)[str(x).find("(")+1:str(x).find("%")+1])
data['Male Population'] = data['Male Population'].map(lambda x: str(x)[str(x).find("(")+1:str(x).find("%")+1])
data = data.drop('populationBySex', axis = 1)

data = data.rename(columns={"medianAge": "Median Age (Years)"})
data['Median Age (Years)'] = data['Median Age (Years)'].map(lambda x: str(x)[str(x).find(":")+1:str(x).find("years")])

data = data.rename(columns={"zipCodes": "Zip Codes"})
data['Zip Codes'] = data['Zip Codes'].map(lambda x: str(x)[str(x).find(":")+1: len(str(x))])
data['Zip Codes'] = data['Zip Codes'].map(lambda x: x[0:6])

data = data.rename(columns={"medianIncome": "Median Income"})
data['Median Income'] = data['Median Income'].map(lambda x: str(x)[str(x).find(":")+1: str(x).find("(")])

data = data.rename(columns={"costOfLiving": "Cost Of Living"})
data['Cost Of Living'] = data['Cost Of Living'].map(lambda x: str(x)[str(x).find(":")+1: str(x).find("(")]) + '/100'






data.to_csv("cleanedCityData.csv", index = False, encoding = 'utf8')