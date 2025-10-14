from django.db import models
from django.core.validators import RegexValidator

class Subject(models.Model):
    """نموذج المواد الدراسية"""
    name = models.CharField(max_length=100, verbose_name="اسم المادة")
    code = models.CharField(max_length=10, unique=True, verbose_name="رمز المادة")
    description = models.TextField(blank=True, verbose_name="وصف المادة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "مادة"
        verbose_name_plural = "المواد"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher(models.Model):
    """نموذج الأساتذة"""
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]
    
    first_name = models.CharField(max_length=50, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=50, verbose_name="اسم العائلة")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="رقم الهاتف يجب أن يكون بالصيغة: '+999999999'. حتى 15 رقم مسموح.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="رقم الهاتف")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
    date_of_birth = models.DateField(verbose_name="تاريخ الميلاد")
    hire_date = models.DateField(verbose_name="تاريخ التوظيف")
    subjects = models.ManyToManyField(Subject, verbose_name="المواد التي يدرسها")
    address = models.TextField(verbose_name="العنوان")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الراتب")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "أستاذ"
        verbose_name_plural = "الأساتذة"
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    """نموذج الطلاب"""
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]
    
    GRADE_CHOICES = [
        ('1', 'الصف الأول'),
        ('2', 'الصف الثاني'),
        ('3', 'الصف الثالث'),
        ('4', 'الصف الرابع'),
        ('5', 'الصف الخامس'),
        ('6', 'الصف السادس'),
        ('7', 'الصف السابع'),
        ('8', 'الصف الثامن'),
        ('9', 'الصف التاسع'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الطالب")
    first_name = models.CharField(max_length=50, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=50, verbose_name="اسم العائلة")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="رقم الهاتف يجب أن يكون بالصيغة: '+999999999'. حتى 15 رقم مسموح.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="رقم الهاتف")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
    date_of_birth = models.DateField(verbose_name="تاريخ الميلاد")
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, verbose_name="الصف")
    enrollment_date = models.DateField(verbose_name="تاريخ التسجيل")
    subjects = models.ManyToManyField(Subject, verbose_name="المواد المسجل بها")
    address = models.TextField(verbose_name="العنوان")
    parent_name = models.CharField(max_length=100, verbose_name="اسم ولي الأمر")
    parent_phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="هاتف ولي الأمر")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
        ordering = ['grade', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Grade(models.Model):
    """نموذج الدرجات"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name="الطالب")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="الأستاذ")
    grade = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
    max_grade = models.DecimalField(max_digits=5, decimal_places=2, default=100, verbose_name="الدرجة العظمى")
    exam_date = models.DateField(verbose_name="تاريخ الامتحان")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "درجة"
        verbose_name_plural = "الدرجات"
        ordering = ['-exam_date']
        unique_together = ['student', 'subject', 'exam_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.grade}/{self.max_grade}"
    
    @property
    def percentage(self):
        return (self.grade / self.max_grade) * 100

