import sys
from api import APIClient

from ubuntu import Ubuntu
from npm import NPM

def main():
    [username, apikey] = sys.argv[1:]

    client = APIClient(username, apikey)
    scrapers = [NPM(client), Ubuntu(client)]
    results = [s.run() for s in scrapers]
    

if __name__ == '__main__':
    main()