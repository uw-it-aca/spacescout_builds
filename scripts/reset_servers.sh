#!/bin/bash
# reset_servers.sh : Deletes and refreshes all server databases

cd ..

for name in server admin web
do
    cd "$name"_proj
    pwd
    . bin/activate
    rm $name.db
    python manage.py syncdb
    python manage.py migrate
    cd ..
    deactivate
done
