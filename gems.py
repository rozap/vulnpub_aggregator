import re
import os
import shutil
from scraper import Scraper
from subprocess import Popen
import yaml

class Gems(Scraper):

    ruby_to_node = {
        '~>' : '~'
    }

    def get_description(self, link):
        return "foo"

    def convert_version(self, version):
        version = version[1:].replace('"', '').replace("'", '').strip()
        for key, val in self.ruby_to_node.iteritems():
            version = version.replace(key, val)
        return version

    def parse_entry(self, vuln):
        if not vuln.get('patched_versions', False):
            return

        name = vuln['title']
        description = vuln['description']
        url = vuln['url']
        package_name = vuln['gem']

        versions = [self.convert_version(v) for v in vuln['patched_versions']]

        for version in versions:
            self.client.enter_vuln(package_name, version, name, description, url)

    def run(self):
        name = 'ruby-advisory-db'
        location = '/tmp/ruby-vulns'
        shutil.rmtree(location)
        proc = Popen(['git', 'clone', 'https://github.com/rubysec/%s.git' % name, location])
        proc.wait()
        for root, dirs, files in os.walk(os.path.join(location, 'gems')):
            for f in files:
                with open(os.path.join(root, f), 'r') as vuln:
                    self.parse_entry(yaml.load(vuln.read()))

