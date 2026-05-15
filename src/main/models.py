from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生")
    student_number = models.CharField(max_length=150, verbose_name="学籍番号")
    student_name = models.CharField(max_length=150, verbose_name="名前")
    report_content = models.TextField(verbose_name="提出内容")
    grade = models.CharField(max_length=2, verbose_name="評価")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="提出日時")

    def __str__(self):
        return f"{self.student_number} ({self.student_name}) - {self.grade}"
