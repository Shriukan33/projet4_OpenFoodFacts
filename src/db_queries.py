import mysql.connector
from mysql.connector import Error, DatabaseError
from settings_local import ROOT_PASSWORD, DB_NAME


class DataQueries:

    def display_products_from_category(self, category: str) -> list:
        """
        Makes a query to database to print a list of products
        from a given category.
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            cursor = sql.cursor()
            cursor.execute("SELECT * FROM product WHERE pnns_groups_2 LIKE '{}'".format(category))  # noqa
            list_of_id = []
            for row in cursor:
                print("{} - {} (Nutriscore : {})".format(row[0], row[1], row[2].upper()))  # noqa
                list_of_id.append(int(row[0]))

        except Error as e:
            print("Erreur de connexion à MySQL", e)

        except DatabaseError as e:
            print("Erreur lors de la création de la base de données", e)

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()

        return list_of_id

    def display_details_of_product(self, product_id) -> None:
        """
        Displays the details of a product based on its ID.
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            # Get the details of the product from the database
            cursor = sql.cursor()
            cursor.execute(
                """SELECT * FROM product WHERE id = '{}'""".format(
                    product_id))
            row = cursor.fetchone()
            print("""
            {} - {}
            Nutriscore : {}
            URL : {}
            Magasins : {}
            Lieux d'achat : {}
            """.format(
                row[0], row[1], row[2].upper(),
                row[3], row[4], row[5]))

        except Error as e:
            print("Erreur de connexion à MySQL", e)

        except DatabaseError as e:
            print("Erreur lors de la création de la base de données", e)

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()

    def display_alternatives_of_product(self, product_id) -> None:
        """
        Displays an alternative to a given product
        Alternative must have a better nutriscore and be in the same
        pnns_groups_2
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            # Get the details of the product from the database
            cursor = sql.cursor()
            cursor.execute(
                """SELECT * FROM product WHERE id = '{}'""".format(
                    product_id))
            row = cursor.fetchone()

            # Get the details of the alternative from the database
            # The alternative must have a better nutriscore and
            # belong to the same group
            cursor.execute(
                """SELECT * FROM product WHERE nutriscore_grade < '{}' AND pnns_groups_2 = '{}'""".format(  # noqa
                    row[2], row[7]))
            # Pick the 1st row of the result set
            alternative_id = cursor.fetchone()[0]
            print("Voici une alternative à ce produit :\n")
            self.display_details_of_product(alternative_id)

        except Error as e:
            print("Erreur de connexion à MySQL", e)

        except DatabaseError as e:
            print("Erreur lors de la création de la base de données", e)

        except TypeError:
            print("Aucune meilleure alternative trouvée")

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()
