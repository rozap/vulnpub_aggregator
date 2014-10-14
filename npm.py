import requests
from bs4 import BeautifulSoup
import re
from scraper import Scraper

class NPM(Scraper):

    def get_description(self, link):
        soup = BeautifulSoup(requests.get(link).text)
        return soup.find('div', {'class' : 'advisory-description'}).text


    def run(self):
        body = requests.get('https://nodesecurity.io/advisories', verify = False).text
        soup = BeautifulSoup(body)
        for advisory in soup.find_all('li', {'class' : 'advisory'}):
            advisory_title = advisory.find('div', {'class' : 'advisory-title'})
            name = advisory_title.text
            external_link = advisory_title.find('a').get('href')

            right = advisory.find('div', {'class' : 'advisory-right'})

            effects_package = right.find('div', {'class' : 'module-name'}).text
            effects_version = right.find_all('div', {'class' : 'module-version'})[0].text.split(':')[1]
            effects_version = max(effects_version.split('||')).strip().replace(' ', '')
            qualifiers = ['<', '>', '=', '~', '^']
            if not effects_version[0] in qualifiers:
                #default to less than version qualifier
                effects_version = '<' + effects_version

            # description = self.get_description('https://nodesecurity.io%s' % external_link)
            description = 'See external link'

            self.client.enter_vuln(effects_package, effects_version, name, description, external_link)

