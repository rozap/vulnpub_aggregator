

import requests
from bs4 import BeautifulSoup
import re
from scraper import Scraper
from multiprocessing.pool import ThreadPool

class Ubuntu(Scraper):


    def is_advisory(self, link):
        toks = [t for t in link.get('href').split('/') if not t == '']
        if len(toks) < 2:
            return False
        [usn, usn_num] = toks[0:2]
        return usn == "usn" and re.match('usn\-\d+\-\d+', usn_num)


    def get_version(self, text):
        matches = re.match('.*(\d+\.\d+\.\d+).*', text)
        if matches:
            return '>=' + matches.group(1)

        matches = re.match('.*(\d+\.\d+).*', text)
        if matches:
            return '>=' + matches.group(1) + '.0'


        print "Cannot parse version %s" % text

    def get_advisory(self, link):
        try:
            body = requests.get(link).text
            soup = BeautifulSoup(body)

            name = soup.find('h1').text
            h3s = soup.find_all('h3')

            description = name + '\n'
            for h3 in h3s:
                if h3.text.lower() == 'details':
                    p = h3.find_next_sibling()
                    while True:
                        description += ('\n\n' + p.text)
                        p = p.find_next_sibling()
                        if p.name != 'p':
                            break




            name = (':'.join(name.strip().split(':')[1:])).strip()
            name = name + ': ' + h3s[1].find_next_sibling().text.strip()

            effects = []
            dl = soup.find('dl')
            for dd in dl.find_all('dd'):
                [package, version] = dd.find_all('a')

                effects.append({
                        'vulnerable' : False,
                        'name' : package.text,
                        'version' : self.get_version(version.text)
                    })
                # effects = [e for e in effects if e['version']]
            self.client.enter_vuln(name, effects, description, link)
        except:
            print "shit.."

    def run(self):
        for num in range(1, 60):
            body = requests.get('http://www.ubuntu.com/usn/?page=%s' % num).text
            soup = BeautifulSoup(body)
            advisories = [a for a in soup.find_all('a') if self.is_advisory(a)]
            links = ['http://www.ubuntu.com/%s' % a.get('href').strip('/') + '/' for a in advisories]

            pool = ThreadPool(processes=len(advisories))
            pool.map(self.get_advisory, links)

            


