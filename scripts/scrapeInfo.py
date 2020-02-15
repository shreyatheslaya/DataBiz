import requests
from bs4 import BeautifulSoup
import threading
import pandas as pd
# import RandomHeaders
import random

# grey_harvest = imp.load_source('grey_harvest', '~/grey_harvest')

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
    # dimensions = ['cityPopulation', 'populationBySex', 'medianAge', 'zipCodes', 'medianIncome', 'costOfLiving']
    dimensions = ['state', 'city', 'page']
    df = pd.DataFrame(columns=dimensions)

    # base url of the website
    homeURL = 'http://www.city-data.com/city/'

    proxies = []

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
        self.getProxies()
        # self.getAllCities([self.states[0]])
        # self.df.to_csv('out.csv', sep='\t', encoding='utf-8')


    def getProxies(self):
        proxies_doc = requests.get('https://www.sslproxies.org/').content
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            self.proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
            })
        print('Proxies Retrieved\n')

    # make all requests for a state to get an href to every city in every state
    def getAllCities(self, states):
        threads = [threading.Thread(target=self.getCities, args=(state,)) for state in states]
        for thread in threads:
            thread.start()
            for thread in threads:
                thread.join()

    # populate the list of cities in each state
    def getCities(self, state):
        self.citiesPerState[state] = []
        app = '{}.html'.format(state)
        requestURL = self.homeURL + app
        proxy = self.proxies[random.randint(0, len(self.proxies))]
        proxyDict = {'https': 'https://' + proxy['ip'] + ':' + proxy['port']}
        try:
            print(proxyDict)
            print(requestURL)
            r = requests.get(requestURL, proxies=proxyDict, timeout=10)
            r = r.content
            soup = BeautifulSoup(r, features='html.parser')
            tds = soup.find_all('td')
            for td in tds:
                hrefs = td.find_all('a', href=True)
                if hrefs:
                    for href in hrefs:
                        if 'javascript' not in str(href):
                            if '<a href=\"/' not in str(href):
                                self.citiesPerState[state].append(href.get('href'))

                                print(self.citiesPerState)

                                '''
                                thread the gathering of individual city information from every
                                city in the list of cities for a given state
                                '''
                                threads = [threading.Thread(target=self.getCityInfo, args=(state, city,)) for city in self.citiesPerState[state]]
                                for i, thread in enumerate(threads):
                                    thread.start()
                                    for i, thread in enumerate(threads):
                                        thread.join()
        except:
            print('timed out')

    # get the city infor given a city name and a state
    def getCityInfo(self, state, city):
        requestURL = self.homeURL + city
        r = requests.get(requestURL, headers=header)
        r = r.content
        soup = BeautifulSoup(r, features='html.parser')
        self.extractCityInformation(state, city, soup)

    # function to cleanse the soup of the webpage
    def extractCityInformation(self, state, city, soup):
        # cityPopulation = soup.find_all('section', {'class':'city-population'})[0].text
        # populationBySex = soup.find_all('section', {'class':'population-by-sex'})[0].text
        # medianAge = soup.find_all('section', {'class':'median-age'})[0].text
        # zipCodes = soup.find_all('section', {'class':'zip-codes'})[0].text
        # medianIncome = soup.find_all('section', {'class':'median-income'})[0].text
        # costOfLiving = soup.find_all('section', {'class':'cost-of-living-index'})[0].text
        response = {'state' : state,
                    'city'  : city,
                    'page'  : page}
        self.df = self.df.append(response, ignore_index=True)
        # for dimension in self.dimensions:
        #     response[dimension] = dimension
        # for dimension in self.dimensions:
        #     try:
        #         response[dimension] = soup.find_all('section', {'class' : dimension})[0].text
        #     except:
        #         print('ERROR NAN')
        #         response[dimension] = 'NaN'

        # self.df = self.df.append({'cityPopulation'  : response['cityPopulation'],
        #                     'populationBySex'       : response['populationBySex'],
        #                     'medianAge'             : response['medianAge'],
        #                     'zipCodes'              : response['zipCodes'],
        #                     'medianIncome'          : response['medianIncome'],
        #                     'costOfLiving'          : response['costOfLiving']
        #                     }, ignore_index=True)

if __name__ == '__main__':
    i = Importer()
    i.getAllCities([i.states[0]])
