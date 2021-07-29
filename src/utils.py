import requests
import mysql.connector
from mysql.connector import Error, DatabaseError
from settings_local import ROOT_PASSWORD, DB_NAME


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
        print("Connected to mysql !")
        cursor = sql.cursor()
        sql_create_db_query = (
        print("Creating database '{}' ...".format(DB_NAME))
            """CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4';""".format(DB_NAME))  # noqa
        cursor.execute(sql_create_db_query)

    except Error as e:
        print("Error while connecting to MySQL", e)

    except DatabaseError as e:
        print("Error while creating the databse", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()
            print("MySQL connection is closed")


def create_tables(tables: dict) -> None:
    """Creates tables for the OpenFoodFacts database."""

    try:
        sql = mysql.connector.connect(host="localhost",
                                      user="root",
                                      password=ROOT_PASSWORD,
                                      database=DB_NAME)

        cursor = sql.cursor()
        for name, ddl in tables.items():
            cursor.execute(ddl)

    except Error as e:
        print("Error while connecting to MySQL", e)

    except DatabaseError as e:
        print("Error while creating the databse", e)

    finally:
        if sql.is_connected():
            cursor.close()
            sql.close()
            print("MySQL connection is closed")
