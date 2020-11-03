# Proxdiv
First you want to clone the project
```sh
$ git clone https://github.com/ghuinker/proximity-vs-diversity.git
```
Move into the project
```sh
$ cd myproject
```
It is recommended that you create a virtual environment for your django project. This will allow you to isolate your python environmnet and package during development.
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
$ pip install -r requirements.txt
```

You're ready to start the server!
```sh
$ python3 manage.py runserver
```
Your site should now be available at localhost:8000!

Other useful django commands:
```sh
$ python3 manage.py makemigrations # Create migrations after updating models
$ python3 manage.py migrate # Update database with new migrations
$ python3 manage.py check # See if your project is running correctly
```
# Other
10,355,968 nodes