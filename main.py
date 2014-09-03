import sys
from api import APIClient

from ubuntu import Ubuntu
from npm import NPM

def main():
    try:
        if len(sys.argv) == 3:
            server = 'http://localhost:4000'
            [username, apikey] = sys.argv[1:]
        else:
            [username, apikey, server] = sys.argv[1:]
    except:
        print "Usage:"
        print "python main.py <username> <apikey>"
        print "python main.py <username> <apikey> <server>"

        return

    client = APIClient(username, apikey, server)
    scrapers = [NPM(client), Ubuntu(client)]
    results = [s.run() for s in scrapers]
    

if __name__ == '__main__':
    main()