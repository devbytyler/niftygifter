#!/bin/bash

if [ "$1" == "makemigrations" ]; then
  echo "💥 Rebuilding Migrations"
  rm app/migrations/0*.py
  python manage.py makemigrations
  echo "✅ Done"
fi

echo "💥 Rebuilding Database"
set PGPASSWORD=$DB_PASSWORD
if [ "$IS_AWS" == "True" ]; then
  psql postgres -c "DROP DATABASE $DB_DATABASE" -h $DB_HOSTNAME -U $DB_USER
  psql postgres -c "CREATE DATABASE $DB_DATABASE" -h $DB_HOSTNAME -U $DB_USER
else
  psql -U postgres -c "DROP DATABASE gifty"
  psql -U postgres -c "CREATE DATABASE gifty"
fi
echo "🦆 Migrating New Database"
python manage.py migrate
echo "✅ Done"


python manage.py dbseed
python manage.py runserver

# while true; do
#     read -p "Seed the database? (y, n) " yn
#     case $yn in
#         [Yy]* ) python manage.py dbseed; break;;
#         [Nn]* ) break;;
#         * ) echo "Please answer y or n.";;
#     esac
# done

# if [ "$IS_AWS" == "True" ]; then
#   python manage.py runserver 0.0.0.0:80
# else
#   python manage.py runserver
# fi
# if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
#     echo "Your server is running on port 8000."
# else
#     while true; do
#         read -p "Start the server? (y, n) " yn
#         case $yn in
#             [Yy]* ) python manage.py runserver; break;;
#             [Nn]* ) break;;
#             * ) echo "Please answer y or n.";;
#         esac
#     done
# fi

