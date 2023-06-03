#!/bin/sh

# start the container stack
# (assumes the caller has permission to do this)
docker-compose up -d

# wait for the service to be ready
while ! curl --fail --silent --head http://localhost:8000; do
  sleep 1
done

# open the browser window
open http://localhost:8000

echo "====================================================="
echo "Superuser created:"
echo "username: admin"
echo "password: admin"
echo "Or you can register any new user."
echo "====================================================="