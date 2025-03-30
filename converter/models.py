from django.db import models
from django.contrib.auth.models import User  # если будет авторизация

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # опционально
    original_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='converted/')
    original_format = models.CharField(max_length=10)
    target_format = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_file.name} → {self.target_format}"