from django.contrib import admin

from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date']
    search_fields = ['question_text']
    list_filter = ['question_text', 'pub_date']
    ordering = ['-pub_date']  # ordering - orderby
    date_hierarchy = 'pub_date'
    empty_value_display = '-empty-'


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'votes']
    list_filter = ['choice_text', 'question']
    ordering = ['question', '-votes']
    search_fields = ['choice_text', 'question__question_text']
    autocomplete_fields = ['question']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
