from django.contrib import admin
from .models import Form, Question, Option, Response, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', 'order', 'is_required', 'form']
    list_filter = ['question_type', 'is_required', 'form'] 
    search_fields = ['question_text']

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ['question', 'answer_text', 'file_upload', 'image_choice', 'slider_value', 'ranking_value', 'geolocation_value']

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'user', 'id')
    search_fields = ('form__title', 'user')
    inlines = [AnswerInline] 

class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer)
