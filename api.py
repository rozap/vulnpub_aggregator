import requests
import json

class APIClient(object):

    def __init__(self, username, apikey, server):
        print "Client init as %s:%s --> %s" % (username, apikey, server)
        self.username = username
        self.apikey = apikey
        self.server = server


    def get_headers(self):
        return {
            'authentication' : '%s:%s' % (self.username, self.apikey),
            'Content-Type' : 'application/json'
        }


    def api(self, endpoint):
        return self.server + '/api/v1/' + endpoint 

    """
    ex vuln: 
        {
            "description": "foo",
            "name": "baz",
            "effects" : [
                {
                    "name": "some-package-name",
                    "version": "4.2.0",
                    "vulnerable": true
                },
                {
                    "name": "some-package-name",
                    "version": "5.0.0",
                    "vulnerable": false
                },

            ],
            "external_link": "http://some-blog/post"
        }
    """
    def enter_vuln(self, name, effects, description, external_link):
        print "Sending vuln: %s | %s" % (name, ', '.join([e['version'] for e in effects]))
        data = json.dumps({
            'effects' : effects,
            'external_link' : external_link,
            'description' : description, 
            'name' : name
        })
        resp = requests.post(self.api('vulns'), data = data, headers = self.get_headers())
        if resp.status_code != 201:
            print resp.text
        return resp

