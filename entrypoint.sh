#!/bin/sh
#!/bin/sh

# python manage.py collectstatic
# python manage.py makemigrations 
python manage.py migrate 
python manage.py runserver 0.0.0.0:8001
