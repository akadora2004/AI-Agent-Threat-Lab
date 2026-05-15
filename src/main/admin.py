from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_info', 'report_content', 'grade', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'report_content')
    list_select_related = ('user',)

    def student_info(self, obj):
        name = obj.user.first_name or obj.user.get_full_name() or '名前なし'
        return f"{obj.user.username} ({name})"
    student_info.short_description = '学籍番号・名前'
