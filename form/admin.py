from django.contrib import admin
from .models import Question, Response, Answer, UploadedFile, Center, Department

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):   
    list_display = ('id', 'text', 'question_type')
    search_fields = ('text',)
    list_filter = ('question_type',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):  
    list_display = ('id', 'respondent_name', 'respondent_email', 'submitted_at')
    search_fields = ('respondent_name', 'respondent_email')
    list_filter = ('submitted_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):  
    list_display = ('id', 'response', 'question_text', 'text_answer', 'file_answer')
    search_fields = ('question_text', 'text_answer')
    list_filter = ('response',) 

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):  
    list_display = ('id', 'response', 'file', 'uploaded_at')
    search_fields = ('file',)
    list_filter = ('uploaded_at',)

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name')
    search_fields = ('name',)      

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'center')
    search_fields = ('name',)
    list_filter = ('center',)
