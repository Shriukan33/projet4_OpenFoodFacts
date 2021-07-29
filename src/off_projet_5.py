from utils import (create_database_if_doesnt_exist, create_tables,
                   request_to_data, insert_data_into_table,
                   get_json_data_from_api)

# Query to OpenFoodFacts API
json_data = get_json_data_from_api()

create_database_if_doesnt_exist()
create_tables()

data = request_to_data(json_data)
insert_data_into_table("product", data)
