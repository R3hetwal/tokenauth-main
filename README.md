# Token Authentication  
This is a simple project management system where, users can sign up and sign in. 
Each project has an owner, belongs to an department among other fields. 
Each project can have multiple documents with unique identifiers. 

*Simple token based authetication is used.

*The data can also be exported from admin panel in .csv or .xls format.

*Signals have been used to create user profile on user registration.

*Use of serializers and viewsets for user registration and login.

*Use of @property decorator.

*Safe Delete option for users.

*API to fetch full details of an user including his projects, departments, documents and all other info.

*Date filterable APIs to list files uploaded by a user, by a department.

*API to summarise user stats like how many projects user has worked on a certain month of the year.

*API to summarise project data as total projects, complete status, working days, members involved.

## Implementation of celery and redis.
* Created an model to store monthly, annual summary data of the system like total_projects, total_users etc. and update it every night by ruuning a     ascheduled task using celery.
* Added 100000 dummy data rows to the Project table, mark them as active and inactive respetively if their deadline are after or before today as a background task.
* Grouped the 100000 Projects by their created date in each week of a month.

## Implementation of basic WebGIS data formats, conversion between them and use them in postgis.
* Added a point field home_address on User model to store location of an user.
* Added a model ProjectSite to store GIS data of a project. Have included a pointfield for project site coordinates, a polygon for area for the project site, a LineString for way from project site to the home_address of project creator.
