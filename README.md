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

