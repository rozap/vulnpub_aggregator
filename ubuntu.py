

import requests
from bs4 import BeautifulSoup
import re
from scraper import Scraper

class Ubuntu(Scraper):


    def is_advisory(self, link):
        toks = [t for t in link.get('href').split('/') if not t == '']
        if len(toks) < 2:
            return False
        [usn, usn_num] = toks[0:2]
        return usn == "usn" and re.match('usn\-\d+\-\d+', usn_num)


    def get_advisory(self, link):
        body = requests.get(link).text
        soup = BeautifulSoup(body)
        dl = soup.find('dl')

        for dd in dl.find_all('dd'):
            [package, version] = dd.find_all('a')

            name = soup.find('div', {'id' : 'title'}).text

            description = 'See external link'
            for heading in soup.find_all('h3'):
                if heading.text.lower() == 'summary':
                    description = heading.find_next_sibling().text
                    break

            name = (':'.join(name.strip().split(':')[1:])).strip()

            effected_version = '<' + version.text

            self.client.enter_vuln(package.text, effected_version, name, description, link)

    def run(self):
        for num in range(1, 20):
            body = requests.get('http://www.ubuntu.com/usn/?page=%s' % num).text
            soup = BeautifulSoup(body)
            advisories = [a for a in soup.find_all('a') if self.is_advisory(a)]
            for a in advisories:
                self.get_advisory('http://www.ubuntu.com/%s' % a.get('href'))
            


