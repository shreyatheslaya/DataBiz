import requests
from bs4 import BeautifulSoup
import threading
import pandas as pd

class Importer():

    '''
    print(cityPopulation)
    print(populationBySex)
    print(medianAge)
    print(zipCodes)
    print(medianIncome)
    print(costOfLiving)
    '''

    # pandas dataframe that we are goin to add all city data to
    df = pd.DataFrame(columns=['cityPopulation', 'populationBySex', 'medianAge', 'zipCodes', 'medianIncome', 'costOfLiving'])

    # base url of the website
    homeURL = 'http://www.city-data.com/city/'

    # list of states to iterate through to get cities
    states = [  "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
                "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
                "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
                "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
                "Nebraska","Nevada","New-Hampshire","New-Jersey","New Mexico","New York",
                "North-Carolina","North-Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
                "Rhode-Island","South Carolina","South-Dakota","Tennessee","Texas","Utah",
                "Vermont","Virginia","Washington","West-Virginia","Wisconsin","Wyoming"]

    citiesPerState = {}

    def __init__(self):
        # self.makeAllRequests(self.states)
        self.getAllCities(self.states[0])

    # populate the list of cities in each state
    def getCities(self, state):
        self.citiesPerState[state] = []
        app = '{}.html'.format(state)
        requestURL = self.homeURL + app
        r = requests.get(requestURL)
        r = r.content
        soup = BeautifulSoup(r)
        tds = soup.find_all('td')
        for td in tds:
            hrefs = td.find_all('a', href=True)
            if hrefs:
                for href in hrefs:
                    if 'javascript' not in str(href):
                        if '<a href=\"/' not in str(href):
                            self.citiesPerState[state].append(href.get('href'))
        self.getCityInfo(state, self.citiesPerState[state][0])


    # make all requests for a state to get an href to every city in every state
    def getAllCities(self, states):
        threads = [threading.Thread(target=self.makeRequest, args=(state,)) for state in states]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def getCityInfo(self, state, city):
        requestURL = self.homeURL + self.citiesPerState[state][0]
        r = requests.get(requestURL)
        r=r.content
        soup = BeautifulSoup(r)
        self.handleSoup(soup)

    # function to cleanse the soup of the webpage
    def handleSoup(self, soup):
        cityPopulation = soup.find_all('section', {'class':'city-population'})[0].text
        populationBySex = soup.find_all('section', {'class':'population-by-sex'})[0].text
        medianAge = soup.find_all('section', {'class':'median-age'})[0].text
        zipCodes = soup.find_all('section', {'class':'zip-codes'})[0].text
        medianIncome = soup.find_all('section', {'class':'median-income'})[0].text
        costOfLiving = soup.find_all('section', {'class':'cost-of-living-index'})[0].text
        df_marks = df_marks.append(new_row, ignore_index=True)
        # newRow = {}
        self.df = df.append({'cityPopulation'   : cityPopulation,
                            'populationBySex'   : populationBySex,
                            'medianAge'         : medianAge,
                            'zipCodes'          : zipCodes,
                            'medianIncome'      : medianIncome,
                            'costOfLiving'      : costOfLiving
                            })
        print(cityPopulation)
        print(populationBySex)
        print(medianAge)
        print(zipCodes)
        print(medianIncome)
        print(costOfLiving)

if __name__ == '__main__':
    i = Importer()
