#!/bin/sh

# start the container stack
# (assumes the caller has permission to do this)
docker-compose build --no-cache
docker compose up

# wait for the service to be ready
while ! curl --fail --silent --head http://localhost:5000; do
  sleep 1
done

# open the browser window
open http://localhost:5000
#echo "visit http://localhost:5000"

echo "====================================================="
echo "Superuser created:"
echo "username: admin"
echo "password: admin"
echo "Or you can register any new user."
echo "====================================================="