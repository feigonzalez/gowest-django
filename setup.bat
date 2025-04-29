pip install django
pip install Pillow
pip install djangorestframework
pip install requests
pip install cx_oracle
sqlplus
:: sys as sysdba
:: system
:: @prepareDB.sql
:: exit
cd gowest
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
:: gowest_admin
:: gowest_admin@gowest.com
:: gowest
:: gowest
:: y
cd ..
sqlplus
:: gowest_admin
:: gowest
:: @popDB.sql
:: exit
cd gowest
python manage.py runserver