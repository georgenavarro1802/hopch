from django.contrib import admin


# Register your models here.
from app.models import Challenges, Questions, Responses


class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created')
    search_fields = ('name', 'code')

admin.site.register(Challenges, ChallengesAdmin)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'text', 'created', 'answer1', 'answer2', 'answer3', 'answer4')
    search_fields = ('challenge__name', 'text')

admin.site.register(Questions, QuestionsAdmin)


class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('question', 'created',
                    'response_answer1', 'response_answer2', 'response_answer3', 'response_answer4')
    search_fields = ('question__text', )

admin.site.register(Responses, ResponsesAdmin)
