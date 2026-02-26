from django.contrib import admin  # type: ignore

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ('pub_date',)
    ordering = ('pub_date',)
    search_fields = ('question_text',)
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]



class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes')
    list_filter = ('votes',)
    ordering = ('votes',)
    search_fields = ('choice_text',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

