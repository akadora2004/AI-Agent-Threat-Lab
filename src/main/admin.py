from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_number', 'student_name', 'report_content', 'grade', 'created_at')
    search_fields = ('student_number', 'student_name', 'report_content')
    list_select_related = ('user',)
