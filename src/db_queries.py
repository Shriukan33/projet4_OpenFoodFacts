import mysql.connector
from mysql.connector import Error, DatabaseError
from settings_local import ROOT_PASSWORD, DB_NAME


class DataQueries:

    def display_products_from_category(self, category: int) -> list:
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
            cursor.execute("SELECT * FROM product WHERE pnns_groups_2 = {}".format(int(category)))  # noqa
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
                """SELECT * FROM product WHERE nutriscore_grade < '{}' AND pnns_groups_2 = '{}' ORDER BY nutriscore_grade""".format(  # noqa
                    row[2], row[7]))
            # Displays top 3 alternatives
            alternative_id = cursor.fetchmany(3)
            if len(alternative_id) > 0:
                print(f"Voici {len(alternative_id)} alternatives :")

            for i in range(3):
                try:
                    print("\n")
                    self.display_details_of_product(alternative_id[i][0])
                except IndexError:
                    # If there are no alternatives or less than 3.
                    print("Aucune autre alternative trouvée.")
                    break

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

    def save_product_to_saved_table(self, product_id):
        """
        Saves a product to saved table.
        Users can save products they want to replace.
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            cursor = sql.cursor()
            # cursor.execute("""SELECT (id)
            # FROM saved
            # WHERE id = '{}'""".format(product_id))
            # row = cursor.fetchone()
            cursor.execute(
                f"""INSERT INTO saved (id)
                VALUES({product_id})""")

            sql.commit()
            print("Sauvegarde effectuée !")

        except Error as e:
            if e.errno == 1062:
                print("Cette produit est déjà enregistré.")
            else:
                print("Erreur lors de la sauvegarde de l'article : ", e)

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()

    def display_saved_results(self) -> list:
        """
        Display the list of saved products in the saved table.
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            cursor = sql.cursor()
            cursor.execute("SELECT * FROM saved")
            list_of_id = []
            # Make a list of ID to display the details.
            for row in cursor:
                list_of_id.append(int(row[0]))

            if len(list_of_id) > 0:
                print(f"Voici {len(list_of_id)} produits sauvegardés :\n")
                for product_id in list_of_id:
                    self.display_oneline_details(product_id)
            else:
                print("Aucun produit sauvegardé.\n")

        except Error as e:
            print("Erreur de connexion à MySQL", e)

        except DatabaseError as e:
            print("Erreur lors de la création de la base de données", e)

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()

        return list_of_id

    def display_oneline_details(self, product_id: int) -> None:
        """
        Displays short description of a product using its ID
        Shows with this format : product_id - product_name - nutriscore_grade
        """
        try:
            sql = mysql.connector.connect(host="localhost",
                                          user="root",
                                          password=ROOT_PASSWORD,
                                          database=DB_NAME)

            cursor = sql.cursor()
            cursor.execute(
                """SELECT * FROM product WHERE id = '{}'""".format(
                    product_id))
            row = cursor.fetchone()
            print("""{} - {} - Nutriscore : {}""".format(
                row[0], row[1], row[2].upper()))

        except Error as e:
            print("Erreur de connexion à MySQL", e)

        except DatabaseError as e:
            print("Erreur lors de la création de la base de données", e)

        finally:
            if sql.is_connected():
                cursor.close()
                sql.close()
