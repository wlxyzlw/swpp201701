pip3 install requests
rm db.sqlite3
python manage.py migrate
python manage.py shell < inittest.py
