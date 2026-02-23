from django.contrib import admin  # type: ignore

from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)