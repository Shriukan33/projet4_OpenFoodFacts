# Utilisez les données publiques de l'OpenFoodFacts

This repository contains the code of OpenClassRooms' project 5.

This command line interface allows the user to search for products and find their alternatives, if any. 

Users can save the search results to lconsult them later. 

## Requirements 
- Python 3
- MySQL
- Git

## Installation

### 1. Change current directory to be where you want the project to be
    cd <future project folder> 
 
### 2. Clone the github project
    git clone https://github.com/Shriukan33/projet_5_OpenFoodFacts.git

### 3. Get into the project's folder
    cd projet_5_OpenFoodFacts

### 4. Create a virtual environnement (recommended)
    python -m venv venv

### 5. Activate your virtual environnement (if you went through step 4)
#### Windows
    venv/Scripts/activate
#### Linux / MacOS
    . venv/bin/activate

### 6. Install project's depedencies
    pip install -r requirements.txt

### 7. Complete the config file "settings_local.py"
In order to connect and create a database in MySQL, the script requires that you enter 
your password for the `root` user inside the `ROOT_PASSWORD` constant at line 2 of `src/settings_local.py`

You can also modify the name of the created database with `DB_NAME` if you like, by default this is `off_database`.

## Running the app

You're now ready to run the app ! 

Two options, you can : 
* Create the database without launching the main script by simply launching `python src/db_setup.py`
* Or launch directly the `src/main.py` to create the database if needed and then start looking for alternatives. 


### Main menu

You're presented 3 options : 
* 1. Replace a product
* 2. See your saved results 
* 3. Exit the app

#### Replace a product

Replacing a product is a multistep process: 
* You first need to pick the category of your product, among the 5 most popular ones in France. This will display the list of available products you can replace.

    ID - Name of the product - Nutriscore grade

* Then you enter the ID of the product you want to replace, this is the leftmost number. 
* You're presented up to 3 alternatives to this product, it's possible that your product has less than 3 better alternatives (Nutriscore wise), or has none.
* You can choose to save this result for later and easier consultation.

#### See saved results
If you saved results before, you can now see a simplified version of the product you saved results for. 

You can then choose to display results, or simple go back to main menu. 

If you want to display a saved results, entering the ID will display the alternatives the same way it did in the replace product section. 

#### Exit the app

Terminates your instance. But don't worry, the database doesn't need to be created again, and saved results will stay. 

