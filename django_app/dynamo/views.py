from importlib import reload, import_module
from django.contrib import messages, admin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.apps import apps
from django.urls import clear_url_caches
from django.conf import settings
from django.db.utils import IntegrityError
from dynamic_models.models import ModelSchema, FieldSchema


class CreateModelView(View):
	def get(self, request):
		return render(request, "dynamo/create_model.html")

	def post(self, request):
		model_name = request.POST.get("model_name")
		if not model_name:
			messages.error(request, "Please provide model name")
		try:
			new_schema = ModelSchema.objects.create(name=model_name)

			fields = (len(request.POST) - 2) // 2
			added_fields = []
			for i in range(1, fields + 1):
				field_name = request.POST.get(f"name_field_{i}")
				if field_name and field_name not in added_fields:
					FieldSchema.objects.create(
						name=field_name,
						data_type=request.POST.get(f"type_field_{i}"),
						model_schema=new_schema,
					)

			NewModel = new_schema.as_model()

			admin.site.register(NewModel)
			reload(import_module(settings.ROOT_URLCONF))
			clear_url_caches()

			messages.success(request,
							 f"Model {NewModel.__name__} sucessfully created. You can navigate to 'Dynamo/List Models'")
		except IntegrityError:
			messages.error(request, "Model with such name already exists!")
		return redirect(reverse_lazy("dynamo:create_model"))


class ListModelsView(View):
	def get(self, request):
		all_models = apps.get_models()
		dyno_models = [model.__name__ for model in all_models if model._meta.app_label == 'dynamo']
		return render(request, "dynamo/list_models.html", context={"dyno_models": dyno_models})
