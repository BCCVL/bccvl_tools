import requests
import sys, os
import urllib
import csv

SDMDEMO_URL = "{bccvlurl}/experiments/API/em/v1/demosdm"
ALA_SPECIES_DL_URL = "http://bie.ala.org.au/ws/download?q=rank:species&fields=guid,scientificName&fq=rk_kingdom:{kingdom}"

def run_sdmdemo(bccvl_url, kingdom_name):
 
    # TODO: validate kingdom
    # Download species record for the kingdom specified.
    id_list = []

    try:
        species_file, _ = urllib.urlretrieve(ALA_SPECIES_DL_URL.format(kingdom=kingdom_name))
        with open(species_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            # skip header
            next(csv_reader)

            # Run sdmdemo for each species in the kingdom.
            demosdm_url = SDMDEMO_URL.format(bccvlurl=bccvl_url)
            username = os.environ.get('BCCVL_USERNAME')
            password = os.environ.get('BCCVL_PASSWORD')

            if username is None or password is None:
                print "The environment variable BCCVL_USERNAME or BCCVL_PASSWORD are not set."
                return id_list

            # TODO: Check if species has occurrence record before start a sdmdemo.
            for row in csv_reader:
                lsid = row[0]
                if lsid:
                    response = requests.request("POST", demosdm_url, auth=(username, password), params={"lsid": lsid}, verify=False)
                    id_list.append(lsid)
    finally:
        if species_file:
            os.remove(species_file)

    return id_list

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: {} <BCCVL_URL> <species_kingdom>".format(sys.argv[0])
        exit(-1)

    # TODO: Validate kingdom
    # Run sdmdemo for each species in the kingdom specified
    lsidlist = run_sdmdemo(bccvl_url=sys.argv[1], kingdom_name=sys.argv[2])
    print len(lsidlist)

