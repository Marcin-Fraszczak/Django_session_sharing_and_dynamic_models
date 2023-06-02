from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		self.fields.pop('password2')

	shared = forms.BooleanField(required=False)
	class Meta:
		model = get_user_model()
		fields = ["username", "password1", "shared"]


class CustomUserLoginForm(AuthenticationForm):
	shared = forms.BooleanField(required=False)
	class Meta:
		model = get_user_model()
		fields = ["username", "password", "shared"]