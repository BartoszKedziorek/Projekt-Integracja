python ./DatasetsPythonClient/load_countries.py;
python ./DatasetsPythonClient/DatasetsClient.py;
python manage.py migrate users
python manage.py runserver 0.0.0.0:8000;