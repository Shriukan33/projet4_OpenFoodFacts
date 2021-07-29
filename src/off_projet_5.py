import requests

from utils import create_database_if_doesnt_exist

# Query to OpenFoodFacts API
json_data = get_json_data_from_api()

create_database_if_doesnt_exist()
