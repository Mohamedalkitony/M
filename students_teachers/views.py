from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from .models import Student, Teacher, Subject, Grade

def home(request):
    """الصفحة الرئيسية"""
    # إحصائيات عامة
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_subjects = Subject.objects.count()
    total_grades = Grade.objects.count()
    
    # أحدث الطلاب المسجلين
    recent_students = Student.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # أحدث الأساتذة
    recent_teachers = Teacher.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'total_grades': total_grades,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
    }
    return render(request, 'students_teachers/home.html', context)

def students_list(request):
    """قائمة الطلاب"""
    search_query = request.GET.get('search', '')
    grade_filter = request.GET.get('grade', '')
    
    students = Student.objects.filter(is_active=True)
    
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    
    if grade_filter:
        students = students.filter(grade=grade_filter)
    
    students = students.order_by('grade', 'first_name', 'last_name')
    
    # تقسيم النتائج إلى صفحات
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # خيارات الصفوف للفلترة
    grade_choices = Student.GRADE_CHOICES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'grade_filter': grade_filter,
        'grade_choices': grade_choices,
    }
    return render(request, 'students_teachers/students_list.html', context)

def student_detail(request, student_id):
    """تفاصيل الطالب"""
    student = get_object_or_404(Student, id=student_id, is_active=True)
    grades = Grade.objects.filter(student=student).order_by('-exam_date')
    
    # حساب المعدل العام
    avg_grade = grades.aggregate(avg=Avg('grade'))['avg']
    
    context = {
        'student': student,
        'grades': grades,
        'avg_grade': avg_grade,
    }
    return render(request, 'students_teachers/student_detail.html', context)

def teachers_list(request):
    """قائمة الأساتذة"""
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    
    teachers = Teacher.objects.filter(is_active=True)
    
    if search_query:
        teachers = teachers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if subject_filter:
        teachers = teachers.filter(subjects__id=subject_filter)
    
    teachers = teachers.order_by('first_name', 'last_name').distinct()
    
    # تقسيم النتائج إلى صفحات
    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # المواد للفلترة
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'subjects': subjects,
    }
    return render(request, 'students_teachers/teachers_list.html', context)

def teacher_detail(request, teacher_id):
    """تفاصيل الأستاذ"""
    teacher = get_object_or_404(Teacher, id=teacher_id, is_active=True)
    subjects = teacher.subjects.all()
    
    # الطلاب الذين يدرس لهم
    students_count = Student.objects.filter(subjects__in=subjects, is_active=True).distinct().count()
    
    # الدرجات التي أدخلها
    grades_count = Grade.objects.filter(teacher=teacher).count()
    
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'students_count': students_count,
        'grades_count': grades_count,
    }
    return render(request, 'students_teachers/teacher_detail.html', context)

def subjects_list(request):
    """قائمة المواد"""
    subjects = Subject.objects.all().order_by('name')
    
    # إضافة إحصائيات لكل مادة
    for subject in subjects:
        subject.students_count = subject.student_set.filter(is_active=True).count()
        subject.teachers_count = subject.teacher_set.filter(is_active=True).count()
    
    context = {
        'subjects': subjects,
    }
    return render(request, 'students_teachers/subjects_list.html', context)

def subject_detail(request, subject_id):
    """تفاصيل المادة"""
    subject = get_object_or_404(Subject, id=subject_id)
    teachers = subject.teacher_set.filter(is_active=True)
    students = subject.student_set.filter(is_active=True)
    grades = Grade.objects.filter(subject=subject).order_by('-exam_date')
    
    # إحصائيات المادة
    avg_grade = grades.aggregate(avg=Avg('grade'))['avg']
    
    context = {
        'subject': subject,
        'teachers': teachers,
        'students': students,
        'grades': grades[:10],  # أحدث 10 درجات
        'avg_grade': avg_grade,
    }
    return render(request, 'students_teachers/subject_detail.html', context)

def grades_list(request):
    """قائمة الدرجات"""
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    
    grades = Grade.objects.all()
    
    if search_query:
        grades = grades.filter(
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(student__student_id__icontains=search_query)
        )
    
    if subject_filter:
        grades = grades.filter(subject__id=subject_filter)
    
    grades = grades.order_by('-exam_date')
    
    # تقسيم النتائج إلى صفحات
    paginator = Paginator(grades, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # المواد للفلترة
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'subjects': subjects,
    }
    return render(request, 'students_teachers/grades_list.html', context)

