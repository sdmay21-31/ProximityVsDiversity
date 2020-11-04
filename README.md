# Proximity Vs Diversity

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Other](#other)

Getting Started
=====
First you want to clone the project
```sh
$ git clone https://github.com/ghuinker/proximity-vs-diversity.git
```
Move into the project
```sh
$ cd ProximityVsDiversity
```
Now make a copy of the .env.example and name it .env
```sh
$ cp .env.example .env
```
Then go to [This Site](https://miniwebtool.com/django-secret-key-generator/) to create a SECRET_KEY that you will put in your .env file.

Next, it is recommended that you create a virtual environment for your django project. This will allow you to isolate your python environmnet and package during development.
```sh
$ python3 -m pip install virtualenv
$ python3 -m venv environment_name
```
For environment_name I prefer to use ".venv", so it is at the top of my project structure and out of the way. 
##### DON'T FORGET TO ADD "environment_name/" to .gitignore
Enter python environment
Mac and Linux:
```sh
$ source environment_name/bin/activate
```
Windows:
```sh
$ source environment_name/Scripts/activate
```
Once in the environment you should see an indicator on Terminal with the name of your virtual environmnet. Now you install backend dependencies.

```sh
$ pip3 install -r requirements.txt
```
Make sure to migrate your database
```sh
$ python3 manage.py migrate
```

You're ready to start the server!
```sh
$ python3 manage.py runserver
```
Your site should now be available at localhost:8000!

Other useful django commands:
```sh
$ python3 manage.py createsuperuser # Create a super user for Django
$ python3 manage.py check # See if your project is running correctly
$ python3 manage.py seed # Seed 10,000 nodes into your database
```
Project Structure
=====
Folders
----
|Folder | Purpose |
| ----- | ------|
| app | This is where the majority of our project will take place. All functional code will be within this folder. To learn more about the contents of this app look at the next section [App Structure](app-structure)|
| Config | Configuration files that won't change often. When referencing the Django documentation this will be considered our Project folder. |
| Datasets | This is where you will put dataset files, everything in this folder is ignored to prevent large files from being uploaded to github. |

App Structure
----
|Folder/File | Purpose |
| ----- | ------|
| migrations/ | This will store generated migration files. These files should not be changed as unforseen erros can cause a lot of problems. |
| templates/ | This is where all html files will go. |
| __init__.py | Designate this folder as a python module |
| admin.py | Register models to the Django Admin |
| algos.py | House the majority of our Algorithm Functions. There should only be business logic in this file, no data logic (i.e. queries) |
| apps.py | Register this folder as a Django app |
| models.py | This is where the Node Model and Manager will exist. The data-logic/complex queries should be within this file to keep data logic seperated from the rest of the project |
| seed.py | Functions to seed to seed the database. |
| tests.py | Testcases for App. |
| utils.py | Random utility functions that are used in multiple places, but have no other logical location |
| views.py | Render our templates. It is a common mistake to make our views very large. Instead a single view should be no longer than 10 lines of code, and all business logic should be housed in seperate location |

Other
=====
10,355,968 nodes in main_table_1.csv
