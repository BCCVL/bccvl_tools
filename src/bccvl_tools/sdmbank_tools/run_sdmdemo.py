import requests
import sys, os
import urllib
import csv

SDMDEMO_URL = "{bccvlurl}/experiments/API/em/v1/demosdm"
ALA_SPECIES_DL_URL = "http://bie.ala.org.au/ws/download?q=rank:species&fields=guid,scientificName&fq=rk_kingdom:{kingdom}"

def get_species_lsids(kingdom_name):
 
    # TODO: validate kingdom
    # Download species record for the kingdom specified.
    id_list = []

    try:
        species_file, _ = urllib.urlretrieve(ALA_SPECIES_DL_URL.format(kingdom=kingdom_name))
        with open(species_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            # skip header
            next(csv_reader)
            # lsid is the first column
            for row in csv_reader:
                lsid = row[0]
                if lsid:
                    id_list.append(lsid)
    finally:
        if species_file:
            os.remove(species_file)

    return id_list


def run_sdmdemo(lsidlist, bccvl_url):
    # TODO: Check if species has occurrence record before start a sdmdemo.
    # Run sdmdemo for each species in the list.
    demosdm_url = SDMDEMO_URL.format(bccvlurl=bccvl_url)
    username = os.environ.get('BCCVL_USERNAME')
    password = os.environ.get('BCCVL_PASSWORD')

    if username is None or password is None:
        print "The environment variable BCCVL_USERNAME or BCCVL_PASSWORD are not set."
        return

    for lsid in lsidlist:
        if lsid:
            response = requests.request("POST", demosdm_url, auth=(username, password), params={"lsid": lsid}, verify=False)

def main():
    if len(sys.argv) < 3:
        print "Usage: {} <BCCVL_URL> <species_kingdom>".format(sys.argv[0])
        exit(-1)

    # TODO: Validate kingdom
    # Run sdmdemo for each species in the kingdom specified
    lsidlist = get_species_lsids(kingdom_name=sys.argv[2])
    run_sdmdemo(lsidlist, bccvl_url=sys.argv[1])

if __name__ == "__main__":
    main()