import requests
import mysql.connector
from mysql.connector import Error, DatabaseError
from settings_local import ROOT_PASSWORD, DB_NAME


def check_database_existence(DB_NAME: str) -> bool:
    """
    Checks if database exists in MySQL.
    Returns True if the database exists.
    DB_NAME is the value of the constant stored in setting_local.py
    """
    try:
        sql = mysql.connector.connect(host="localhost",
                                      user="root",
                                      password=ROOT_PASSWORD,
                                      database="mysql")

        cursor = sql.cursor()
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
        for database in result:
            if database[0] == DB_NAME:
                return True

        return False

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()


def get_json_data_from_api() -> dict:
    print("Gathering data from OpenFoodFacts API...")
    url = "https://fr.openfoodfacts.org/cgi/search.pl?json=true&action=process&sort_by=popularity&page_size=500&page=1&sort_by=unique_scans_n&fields=product_name,nutriscore_grade,url,stores,purchase_places,pnns_groups_1,pnns_groups_2&coutries=france" # noqa
    headers = {"User-Agent": "Projet5 - Linux/ubuntu - Version 1.0"}
    r = requests.get(url, headers=headers)

    # Turn json response into a dict.
    json_data = r.json()
    print("Data collected successfully")
    return json_data


def create_database_if_doesnt_exist():
    """Connects to mysql thanks to config file and create
        a database if it doesn't already exist"""

    try:
        sql = mysql.connector.connect(host="localhost",
                                      user="root",
                                      password=ROOT_PASSWORD,
                                      database="mysql")
        print("Connected to mysql !\n")
        cursor = sql.cursor()
        sql_create_db_query = (
            """CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4';""".format(DB_NAME))  # noqa
        print("Creating database '{}' ...\nDone !".format(DB_NAME))
        cursor.execute(sql_create_db_query)

    except Error as e:
        print("Error while connecting to MySQL", e)

    except DatabaseError as e:
        print("Error while creating the databse", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()


def create_tables() -> None:
    """Creates tables for the OpenFoodFacts database."""

    # Descriptions of the tables
    tables = {}
    tables["product"] = """CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        product_name TEXT,
        nutriscore_grade TEXT,
        url TEXT,
        stores TEXT,
        purchase_places TEXT,
        pnns_groups_1 TEXT,
        pnns_groups_2 TEXT
    );"""
    print("Creating tables into database...")
    try:
        sql = mysql.connector.connect(host="localhost",
                                      user="root",
                                      password=ROOT_PASSWORD,
                                      database=DB_NAME)

        cursor = sql.cursor()
        for name, ddl in tables.items():
            cursor.execute(ddl)

        print("Table(s) created successfully")
    except Error as e:
        print("Error while connecting to MySQL", e)

    except DatabaseError as e:
        print("Error while creating the databse", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()


def request_to_data(json_data: dict) -> list:
    """
    Creates a nested list containing products and all their informations.
    Will ignore incomplete products.

    json_data: json data from the OpenFoodFacts API
    """

    data = []
    for product in json_data["products"]:
        try:
            product_name = product["product_name"]
            nutriscore_grade = product["nutriscore_grade"]
            url = product["url"]
            stores = product["stores"]
            purchase_places = product["purchase_places"]
            pnns_groups_1 = product["pnns_groups_1"]
            pnns_groups_2 = product["pnns_groups_2"]

            data.append([product_name,
                        nutriscore_grade,
                        url,
                        stores,
                        purchase_places,
                        pnns_groups_1,
                        pnns_groups_2])

        except KeyError:
            # If the product doesn't have one of the keys, skip it.
            continue

    return data


def insert_data_into_table(table: str, data: list) -> None:
    """
    Inserts data into a table.
    table: name of the table
    data: list of data to insert.

    data is a list of lists :
        data[0] is the list of attributes of the first product
        data[0][0] is the name of the first product
        data[0][1] is the nutriscore of the first product
        data[0][2] is the url of the first product
        data[0][3] is the list of stores of the first product
        data[0][4] is the list of purchase places of the first product
        data[0][5] is the pnns_groups_1 of the first product
        data[0][6] is the pnns_groups_2 of the first product
    """

    try:
        sql = mysql.connector.connect(host="localhost",
                                      user="root",
                                      password=ROOT_PASSWORD,
                                      database=DB_NAME)
        print("Populating database with OpenFoodFacts...")
        cursor = sql.cursor()
        for row in data:
            cursor.execute(
                "INSERT INTO {} (\
                    product_name,\
                    nutriscore_grade,\
                    url,\
                    stores,\
                    purchase_places,\
                    pnns_groups_1,\
                    pnns_groups_2\
                ) \
                VALUES (%s, %s, %s, %s, %s, %s, %s)".format(table),
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        sql.commit()
        print("Done !")

    except Error as e:
        print("Error while connecting to MySQL", e)

    except DatabaseError as e:
        print("Error while creating the databse", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()
