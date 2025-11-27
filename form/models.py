from django.db import models

class Question(models.Model):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'
    FILE = 'file'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (FILE, 'File Upload'),
    ]

    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    options = models.TextField(blank=True, help_text="Comma-separated options for multiple choice questions")

    def __str__(self):
        return self.text
    
class Response(models.Model):
    respondent_name = models.CharField(max_length=100)
    respondent_email = models.EmailField()
    respondent_center = models.CharField(max_length=100, default=None)
    respondent_attachment_period = models.CharField(max_length=100, blank=True, null=True)
    respondent_department = models.CharField(max_length=100, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.respondent_name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers', default=None)
    question_text = models.CharField(max_length=255, default=None)
    text_answer = models.TextField(blank=True, null=True)
    file_answer = models.FileField(upload_to='answers/', blank=True, null=True)

    def __str__(self):
        return f"Answer {self.id} for Response {self.response.id}"
    
class UploadedFile(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.id} for Response {self.response.id}"

class Center(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.center.name})"