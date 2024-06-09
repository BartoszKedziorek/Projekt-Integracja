env >> /etc/environment
service cron restart
python ./DatasetsPythonClient/load_countries.py;
python ./DatasetsPythonClient/DatasetsClient.py;
python manage.py migrate users

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python manage.py runserver 0.0.0.0:8000;