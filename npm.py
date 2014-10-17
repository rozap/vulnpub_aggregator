import requests
from bs4 import BeautifulSoup
import re
from scraper import Scraper

class NPM(Scraper):

    def get_description(self, link):
        soup = BeautifulSoup(requests.get(link).text)
        return soup.find('div', {'class' : 'advisory-description'}).text


    def get_version(self, right, idx = 0):
        return right.find_all('div', {'class' : 'module-version'})[idx].text\
            .split(':')[1]\
            .replace('x', '0')\
            .strip()


    def run(self):
        body = requests.get('https://nodesecurity.io/advisories', verify = False).text
        soup = BeautifulSoup(body)
        for advisory in soup.find_all('li', {'class' : 'advisory'}):
            advisory_title = advisory.find('div', {'class' : 'advisory-title'})
            name = advisory_title.text
            external_link = advisory_title.find('a').get('href')
            external_link = 'https://nodesecurity.io%s' % external_link

            right = advisory.find('div', {'class' : 'advisory-right'})

            effects_package = right.find('div', {'class' : 'module-name'}).text
            
            description = 'See external link'

            vulnerable_version = self.get_version(right, 0)
            patched_version = self.get_version(right, 1)
            # description = self.get_description('https://nodesecurity.io%s' % external_link)
            effects = [
                {
                    'name' : effects_package,
                    'version' : patched_version,
                    'vulnerable' : False
                },
                {
                    'name' : effects_package,
                    'version' : vulnerable_version,
                    'vulnerable' : True
                }

            ]
            self.client.enter_vuln(name, effects, description, external_link)



