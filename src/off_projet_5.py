from utils import (check_database_existence, create_database_if_doesnt_exist,
                   create_tables, request_to_data, insert_data_into_table,
                   get_json_data_from_api)
from settings_local import DB_NAME


database_already_exists = check_database_existence(DB_NAME)

if not database_already_exists:
    json_data = get_json_data_from_api()

    create_database_if_doesnt_exist()
    create_tables()

    data = request_to_data(json_data)
    insert_data_into_table("product", data)
