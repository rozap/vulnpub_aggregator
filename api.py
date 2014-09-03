import requests

class APIClient(object):

    def __init__(self, username, apikey, server):
        print "Client init as %s:%s --> %s" % (username, apikey, server)
        self.username = username
        self.apikey = apikey
        self.server = server


    def get_headers(self):
        return {
            'authentication' : '%s:%s' % (self.username, self.apikey)
        }


    def api(self, endpoint):
        return self.server + '/api/v1/' + endpoint 

    """
    ex vuln: 
        {
            "description": "foo",
            "name": "baz",
            "effects_package": "some-package-name",
            "effects_version": "4.20",
            "external_link": "http://some-blog/post"
        }
    """
    def enter_vuln(self, package, version, name, description, external_link):
        print "Sending vuln: %s :: %s" % (package, version)
        data = {
            'effects_version' : version, 
            'effects_package' : package,
            'external_link' : external_link,
            'description' : description, 
            'name' : name
        }
        resp = requests.post(self.api('vulns'), data = data, headers = self.get_headers()).text
        # print resp
        return resp

