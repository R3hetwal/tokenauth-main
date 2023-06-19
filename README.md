# Token Authentication  
This is a simple project management system where, users can sign up and sign in. 
Each project has an owner, belongs to an department among other fields. 
Each project can have multiple documents with unique identifiers. 

* Simple token based authetication is used.

* The data can also be exported from admin panel in .csv or .xls format.

* Signals have been used to create user profile on user registration.

* Use of serializers and viewsets for user registration and login.

* Use of @property decorator.

* Safe Delete option for users.

* API to fetch full details of an user including his projects, departments, documents and all other info.

* Date filterable APIs to list files uploaded by a user, by a department.

* API to summarise user stats like how many projects user has worked on a certain month of the year.

* API to summarise project data as total projects, complete status, working days, members involved.

* Management command to assign project status to all existing projects.

* Signal to trigger management command when a new project is created.

* Test Cases also included for testing some functionalities.

## Implementation of celery and redis.
* Created an model to store monthly, annual summary data of the system like total_projects, total_users etc. and update it every night by ruuning a     ascheduled task using celery.
* Added 100000 dummy data rows to the Project table, mark them as active and inactive respetively if their deadline are after or before today as a background task.
* Grouped the 100000 Projects by their created date in each week of a month.

## Implementation of basic WebGIS data formats, conversion between them and use them in postgis.
* Added a point field home_address on User model to store location of an user.
* Added a model ProjectSite to store GIS data of a project. Have included a pointfield for project site coordinates, a polygon for area for the project site, a LineString for way from project site to the home_address of project creator.
* Export project site data to an shapefile (.shp)

## Implementation of Management Command.
* Management command written to assign default project status to every existing project.
* Signal to trigger management command so as to assign default project statuses to any new project as soon as project is created.

   ### Command to run management command
  ```sh
    $ python manage.py create_default_project_status
  ```

## Implementation of Test Cases.
* Test written for testing user login and user registration functionality.
* Test for checking methods as GET, POST, PUT, PATCH, DELETE for Department and Project available.
* Test for checking signal to trigger management command to assign project status to any Project on creation availale.
* Simple pytest included for learning purpose.

  ### Command to run test cases
  * For pytest:
     ```sh
       $ pytest test/test_learn.py
     ```

  * For django test:
    
     Searches for every test available
     ```sh
       $ python manage.py test
     ```
   
     Runs test in test folder
     ```sh
       $ python manage.py test test
     ```
   
     To run test in particular file only
     ```sh
       $ python manage.py test test.test_registration
       $ python manage.py test test.test_login
       $ python manage.py test test.test_projectapi
       $ python manage.py test test.test_departmentapi
       $ python manage.py test test.test_signal
       $ python manage.py test test.test_learn
     ```
  
  
