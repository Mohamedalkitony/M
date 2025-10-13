from django.urls import path
from . import views

app_name = 'students_teachers'

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.home, name='home'),
    
    # الطلاب
    path('students/', views.students_list, name='students_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # الأساتذة
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    
    # المواد
    path('subjects/', views.subjects_list, name='subjects_list'),
    path('subjects/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    
    # الدرجات
    path('grades/', views.grades_list, name='grades_list'),
]

