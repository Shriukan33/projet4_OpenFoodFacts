from db_setup import SetupDatabase
from db_queries import DataQueries
from settings_local import CATEGORIES, CATEGORIES_FR


# Initialize the database
setup = SetupDatabase()
# Class that makes the queries to database.
queries = DataQueries()


while True:
    print("""
    Que voulez vous faire ?
    1. Remplacer un produit
    2. Voir mes recherches sauvegardées
    3. Quitter l'application

    """)
    choice = ""
    while choice != "1" and choice != "2" and choice != "3":
        choice = input("Votre choix: ")

    # Chose "1" to replace a product
    if choice == "1":
        print("Vous voulez remplacer un produit.")
        print("Choisissez la catégorie du produit à remplacer :")
        categories = CATEGORIES
        categories_fr = CATEGORIES_FR

        # Display all categories
        for i, category in enumerate(categories_fr):
            print(f"{i}. {category}")

        # Ask the user to choose a category
        category_choice = ""
        while category_choice not in range(len(categories)):
            category_choice = input("\nVotre choix: ").strip()
            try:
                category_choice = int(category_choice)
            except ValueError:
                print("Entrez un nombre s'il vous plaît")

        # Display all products from the chosen category
        category = category_choice + 1
        category_fr = categories_fr[int(category_choice)]
        print("\nVous voulez remplacer un produit de "
              f"la catégorie {category_fr}")
        print("Voici une list des produits appartenant à cette catégorie :\n")
        list_of_id = queries.display_products_from_category(category)

        print("Lequel voulez vous remplacer ?\n")

        # Ask to the user to choose a product to replace
        chosen_product_id = ""
        while chosen_product_id not in list_of_id:
            chosen_product_id = input("Votre choix: ").strip()
            try:
                chosen_product_id = int(chosen_product_id)
            except ValueError:
                print("Entrez un nombre s'il vous plaît")

        # Displays alternatives to the chosen product, if any
        print(f"Vous voulez remplacer : {chosen_product_id}")
        queries.display_alternatives_of_product(chosen_product_id)

        # Ask to save the chosen product search result
        print("\nVoulez-vous sauvegarder le résultat de cette recherche ?"
              " (O/N)\n")
        choice = ''
        while choice != "o" and choice != "n":
            choice = input("Votre choix: ").strip().lower()
            if choice == "o":
                queries.save_product_to_saved_table(chosen_product_id)
            elif choice == "n":
                print("Retour au menu\n")

    # User wants to see the list of saved products
    elif choice == "2":
        list_of_saved_products = queries.display_saved_results()
        # If products are saved, ask if they want to display the
        # search results.
        if len(list_of_saved_products) > 0:

            choice = ""
            while choice != "o" and choice != "n":
                print("\nVoulez-vous afficher les résultats sauvegardés ?"
                      " (O/N)\n")
                choice = input("Votre choix : ").strip().lower()

            # User wants to see the saved results
            if choice == "o":
                choice = ''
                while choice not in list_of_saved_products:
                    print("\nDe quel produit voulez vous afficher les "
                          "alternatives ?\n")
                    choice = input("\nVotre choix : ").strip()
                    try:
                        choice = int(choice)
                    except ValueError:
                        print("Entrez un nombre s'il vous plaît")
                queries.display_alternatives_of_product(choice)

            # User doesn't want to see the saved results
            elif choice == "n":
                print("\nRetour au menu\n")

    elif choice == "3":
        print("\nAu revoir !")
        break
