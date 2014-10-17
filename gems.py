import re
import os
import shutil
from scraper import Scraper
from subprocess import Popen
import yaml

class Gems(Scraper):

    qualifiers = {
        '=' : '=='
    }

    def convert_version(self, version):
        version = version[1:].replace('"', '').replace("'", '').strip()
        for old, new in self.qualifiers.iteritems():
            version = version.replace(old, new)
        return version

    def make_effect(self, package_name, v, vulnerable):
        return {
            'vulnerable' : vulnerable,
            'name' : package_name,
            'version' : self.convert_version(v)
        }

    def parse_entry(self, vuln):
        if not vuln.get('patched_versions', False):
            return

        name = vuln['title']
        description = vuln['description']
        url = vuln['url']

        package_name = vuln['gem']
        effects = [self.make_effect(package_name, v, False) for v in vuln['patched_versions']] + \
        [self.make_effect(package_name, v, False) for v in vuln.get('unaffected_versions', [])] 
        resp = self.client.enter_vuln(name, effects, description, url)

    def run(self):
        name = 'ruby-advisory-db'
        location = '/tmp/ruby-vulns'
        try:
            shutil.rmtree(location)
        except:
            pass
        proc = Popen(['git', 'clone', 'https://github.com/rubysec/%s.git' % name, location])
        proc.wait()
        for root, dirs, files in os.walk(os.path.join(location, 'gems')):
            for f in files:
                with open(os.path.join(root, f), 'r') as vuln:
                    self.parse_entry(yaml.load(vuln.read()))

