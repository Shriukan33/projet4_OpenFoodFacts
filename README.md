# Utilisez les données publiques de l'OpenFoodFacts

Ce repo sera l'outil qui répond au projet 5 Openclassrooms.
Parcours développeur d'applications Python

## Prérequis 
- Python 3.8
- MySQL

## Paramétrage préalable
Afin d'assurer le bon fonctionnement avec la base de donnée MySQL,
il faudra renseigner localement un fichier **settings_local.py**

Ce dernier contiendra 2 constantes :
* `ROOT_PASSWORD` : Indiquez ici le mot de passe de l'utilisateur "root"
pour accéder à votre compte mysql
* `DB_NAME` : Le nom de la base de donnée que vous souhaitez créer.
