from utils import (check_database_existence, create_database_if_doesnt_exist,
                   create_tables, request_to_data, insert_data_into_table,
                   get_json_data_from_api, display_products_from_category,
                   display_details_of_product, display_alternatives_of_product)
from settings_local import DB_NAME


database_already_exists = check_database_existence(DB_NAME)

if not database_already_exists:
    json_data = get_json_data_from_api()

    create_database_if_doesnt_exist()
    create_tables()

    data = request_to_data(json_data)
    insert_data_into_table("product", data)

print("""
What do you want to do ?
1. Replace a new product
2. See your saved searches.

""")
choice = ""
while choice != "1" and choice != "2":
    choice = input("Your choice: ")

# Chose "1" to replace a product
if choice == "1":
    print("You want to replace a new product\n\
          Pick the category of your product :")
    categories = ["Biscuits and cakes", "Breads", "Breakfast cereals",
                  "Sweets", "Cheese"]

    # Display all categories
    for i, category in enumerate(categories):
        print(f"{i}. {category}")

    # Ask the user to choose a category
    category_choice = ""
    while category_choice not in range(len(categories)):
        category_choice = input("Your choice: ").strip()
        try:
            category_choice = int(category_choice)
        except ValueError:
            print("Please enter a number")

    # Display all products from the chosen category
    category = categories[int(category_choice)]
    print(f"You want to replace a product from {category}")
    print("Here is a list of products from this category :\n\n")
    list_of_id = display_products_from_category(category)

    print("Which one do you want to replace ?\n")

    # Ask to the user to choose a product
    chosen_product_id = ""
    while chosen_product_id not in list_of_id:
        chosen_product_id = input("Your choice: ").strip()
        try:
            chosen_product_id = int(chosen_product_id)
        except ValueError:
            print("Please enter a number")

    print(f"You want to replace the product {chosen_product_id}")
    display_alternatives_of_product(chosen_product_id)
