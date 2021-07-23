import requests

from utils import create_database_if_doesnt_exist

# Query to OpenFoodFacts API
url = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&sort_by=popularity&page_size=10&page=1&sort_by=unique_scans_n&json=true&fields=product_name,nutriscore_grade,code,url,categories,stores,purchase_places,pnns_groups_1,pnns_groups_2&coutries=france" # noqa
headers = {"User-Agent": "Projet5 - Linux/ubuntu - Version 1.0"}
r = requests.get(url, headers=headers)

# Turn json response into a dict.
json_data = r.json()

create_database_if_doesnt_exist()
