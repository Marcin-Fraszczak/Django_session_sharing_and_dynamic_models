# Django + Flask + Redis (Docker needed)
## Simple app to showcase session sharing between Django and Flask

## To run it locally:
1) Clone the repo:

`git clone git@github.com:Marcin-Fraszczak/Django_session_sharing_and_dynamic_models.git`

2) Inside the main directory run:

`sh start.sh`

This script will run docker compose and open the app in the browser when ready.

3) Do not forget to type
`docker compose down`
after finishing.


4) Alternatively you can type `docker compose up` yourself and manually navigate to http://localhost:8000


## How it works?

Django app is responsible for session management, user registration, login, logout.

Client gets only session id in a cookie while the rest is saved to Redis database.

Both Django and Flask are checking client's cookie and look for particular entry in Redis.