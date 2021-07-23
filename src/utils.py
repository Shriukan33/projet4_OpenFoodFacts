import mysql.connector
from mysql.connector import Error, DatabaseError
from settings_local import ROOT_PASSWORD, DB_NAME


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
            """CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8';""".format(DB_NAME))  # noqa
        print("Creating database '{}' ...".format(DB_NAME))
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
