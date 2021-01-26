# django_tutorial 

Simple REST Api Quiz based on the instructions provided on the offical page of Djando documentation. 
Enables adding, editing and removing questions to the quiz and also answering to them by the user. 

# Technologies

 - Django
 - SQLite

# In order to open the project, follow the below steps: 
 Install the virtual environment: 
 - pip3 install virtualenv
 - virtualenv -p python3 env
 - source env/bin/activate
 
 Install and start django project: 
 - pip install django
 - django-admin startproject <name>
 - python manage.py startapp polls
 - python manage.py runserver
  
 After that make the required migrations: 
 - python manage.py makemigrations <name>
 - python manage.py migrate
 

