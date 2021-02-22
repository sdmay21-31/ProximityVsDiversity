#! /bin/bash
git pull origin master || exit 3

pip3 install -r requirements.txt

python3 manage.py migrate

python3 manage.py collectstatic --noinput

sudo systemctl restart gunicorn