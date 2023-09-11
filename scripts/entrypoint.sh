python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

gunicorn -c gunicorn.conf.py sleepwalker.wsgi --preload