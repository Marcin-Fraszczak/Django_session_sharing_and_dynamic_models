from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomUserCreationForm, CustomUserLoginForm
import redis

redis_db = redis.StrictRedis(host='localhost', port=6379)

User = get_user_model()


def set_redis(session_key, username, is_shared):
	redis_db.set(session_key, username)
	redis_db.set(f"{session_key}_shared", [0, 1][is_shared])


def logout_current_user(request):
	try:
		session_key = getattr(request.session, "_session_key")
		redis_db.delete(*[session_key, f"{session_key}_shared"])
	except redis.exceptions.DataError:
		pass
	if request.user.is_authenticated:
		logout(request)


class RegisterView(View):
	def get(self, request):
		form = CustomUserCreationForm()
		return render(request, "registration/register.html", context={"form": form})

	def post(self, request):
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			logout_current_user(request)
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			is_shared = form.cleaned_data.get('shared')
			exists = User.objects.filter(username=username).first()
			if not exists:
				new_user = User(username=username)
				new_user.set_password(password)
				new_user.save()
				user = authenticate(username=username, password=password)
				login(request, user)
				session_key = getattr(request.session, "_session_key")
				set_redis(session_key, username, is_shared)
				return redirect("accounts:home")
			else:
				messages.error(request, "User with that username already exists.")
		else:
			messages.error(request, "Invalid input, try again.")

		form = CustomUserCreationForm()
		return render(request, "registration/register.html", context={"form": form})


class LoginView(View):
	def get(self, request):
		form = CustomUserLoginForm()
		return render(request, "registration/login.html", context={"form": form})

	def post(self, request):
		form = CustomUserLoginForm(request, data=request.POST)
		if form.is_valid():
			logout_current_user(request)
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			is_shared = form.cleaned_data.get('shared')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				session_key = getattr(request.session, "_session_key")
				if session_key:
					set_redis(session_key, username, is_shared)
				redirect_url = request.GET.get("next")
				if not redirect_url:
					return redirect(reverse_lazy("accounts:home"))
				return redirect(redirect_url)
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")
		form = CustomUserLoginForm()
		return render(request, "registration/login.html", context={"form": form})


class HomeView(View):
	def get(self, request):
		session_key = getattr(request.session, "_session_key")
		try:
			is_shared = int(redis_db.get(f"{session_key}_shared").decode('utf-8'))
		except (redis.exceptions.DataError, AttributeError):
			is_shared = None
		return render(request, 'home.html', context={"is_shared": is_shared})


class LogoutView(View):
	def get(self, request):
		logout_current_user(request)
		redirect_url = request.GET.get('next')
		if redirect_url:
			return redirect(redirect_url)
		return redirect("/")
