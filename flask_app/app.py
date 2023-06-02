from flask import Flask, request, render_template
import redis
from os import getenv

app = Flask(__name__)

app.secret_key = 'django-insecure-sp#slpf7#7o9+1#^y-tirwcug+-y&l_1($%evub1afjf0*z(=)'

redis_host = getenv("redis_host", default="localhost")
redis_db = redis.StrictRedis(host=redis_host, port=6379)

dj_base = "http://127.0.0.1:8000"


@app.route('/', methods=['GET'])
def home_view():
	session_key = request.cookies.get('sessionid')
	try:
		username = redis_db.get(session_key).decode('utf-8')
		is_shared = int(redis_db.get(f"{session_key}_shared").decode('utf-8'))
	except (redis.exceptions.DataError, AttributeError):
		username, is_shared = None, None
	ctx = {
		"username": username,
		"is_shared": is_shared,
		"login": f"{dj_base}/accounts/login?next=http://127.0.0.1:5000",
		"logout": f"{dj_base}/accounts/logout",
		"register": f"{dj_base}/accounts/register",
		"home": f"{dj_base}"
	}
	# if not (session_key and username):
	# 	return redirect(ctx['login'])

	return render_template('home.html', **ctx)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port='5000')
