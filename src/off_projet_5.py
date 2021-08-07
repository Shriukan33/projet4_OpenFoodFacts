from db_setup import SetupDatabase
from db_queries import DataQueries

# Initialize the database
setup = SetupDatabase()
# Class that makes the queries to database.
queries = DataQueries()

print("""
Que voulez vous faire ?
1. Remplacer un produit
2. Voir mes recherches sauvegardées

""")
choice = ""
while choice != "1" and choice != "2":
    choice = input("Votre choix: ")

# Chose "1" to replace a product
if choice == "1":
    print("Vous voulez remplacer un produit.")
    print("Choisissez la catégorie du produit à remplacer :")
    categories = ["Biscuits and cakes", "Breads", "Breakfast cereals",
                  "Sweets", "Cheese"]
    categories_fr = ["Biscuits et gâteaux", "Pains",
                     "Céréales", "Bonbons", "Fromages"]

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
    category = categories[int(category_choice)]
    category_fr = categories_fr[int(category_choice)]
    print(f"\nVous voulez remplacer un produit de la catégorie {category_fr}")
    print("Voici une list des produits appartenant à cette catégorie :\n")
    list_of_id = queries.display_products_from_category(category)

    print("Lequel voulez vous remplacer ?\n")

    # Ask to the user to choose a product
    chosen_product_id = ""
    while chosen_product_id not in list_of_id:
        chosen_product_id = input("Votre choix: ").strip()
        try:
            chosen_product_id = int(chosen_product_id)
        except ValueError:
            print("Entrez un nombre s'il vous plaît")

    print(f"Vous voulez remplacer : {chosen_product_id}")
    queries.display_alternatives_of_product(chosen_product_id)
