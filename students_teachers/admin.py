from django.contrib import admin
from .models import Subject, Teacher, Student, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'gender', 'hire_date', 'is_active']
    list_filter = ['gender', 'hire_date', 'is_active', 'subjects']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['subjects']
    fieldsets = (
        ('المعلومات الشخصية', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth', 'address')
        }),
        ('معلومات العمل', {
            'fields': ('hire_date', 'subjects', 'salary', 'is_active')
        }),
    )
    ordering = ['first_name', 'last_name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'grade', 'email', 'phone', 'enrollment_date', 'is_active']
    list_filter = ['grade', 'gender', 'enrollment_date', 'is_active', 'subjects']
    search_fields = ['first_name', 'last_name', 'student_id', 'email']
    filter_horizontal = ['subjects']
    fieldsets = (
        ('المعلومات الشخصية', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth', 'address')
        }),
        ('معلومات الدراسة', {
            'fields': ('grade', 'enrollment_date', 'subjects', 'is_active')
        }),
        ('معلومات ولي الأمر', {
            'fields': ('parent_name', 'parent_phone')
        }),
    )
    ordering = ['grade', 'first_name', 'last_name']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'teacher', 'grade', 'max_grade', 'percentage', 'exam_date']
    list_filter = ['subject', 'teacher', 'exam_date']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name', 'teacher__first_name', 'teacher__last_name']
    ordering = ['-exam_date']
    
    def percentage(self, obj):
        return f"{obj.percentage:.1f}%"
    percentage.short_description = "النسبة المئوية"

# تخصيص عنوان موقع الإدارة
admin.site.site_header = "نظام إدارة الطلاب والأساتذة"
admin.site.site_title = "إدارة المدرسة"
admin.site.index_title = "لوحة التحكم"

