from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import math
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import Q
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The Employee ID field must be set")
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # approved = models.BooleanField(('Approved'), default = False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        permissions = [
            ("view_manager_pages", "Can view manager pages"),
            ("view_employee_pages", "Can view employee pages"),
        ]
    # def save(self, *args, **kwargs):
    #     if not self.user_id:
    #         last_id = CustomUser.objects.order_by('-user_id').first()
    #         if last_id:
    #             last_id = int(last_id.user_id[4:]) + 1
    #         else:
    #             last_id = 1
    #         self.user_id = f'ACT{str(last_id).zfill(3)}'
    #     super().save(*args, **kwargs)# This is to get the full name of a user where is_manager=True

    # def get_department_heads(self):
    #     return self.filter(Q(is_manager=True) & Q(first_name__isnull=False) & Q(last_name__isnull=False))


# class DepartmentHeadField(models.ForeignKey):
#     def __init__(self, **kwargs):
#         kwargs['to'] = CustomUser
#         kwargs['on_delete'] = models.SET_NULL
#         kwargs['related_name'] = 'head_of_department'
#         kwargs['blank'] = True
#         kwargs['null'] = True
#         super().__init__(**kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super().deconstruct()
    #     del kwargs['to']
    #     return name, path, args, kwargs

    def __str__(self):
        return self.user_id


# Departments Model
class Department(models.Model):
    department_name = models.CharField(max_length=100, null=True)
    department_head = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='head_of_department', blank=True, null=True)
    # department_head = DepartmentHeadField()
    # total_employees = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def total_employees(self):
        total_employees = Employee.objects.filter(department=self).count()
        return total_employees

    def __str__(self):
        return self.department_name

# Designation Model


class Designation(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, related_name='designations', null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.job_title

# Employee Register Model


class ActiveEmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status='In')


class Employee(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )

    EMPLOYMENT_TYPE_CHOICES = (
        ('fulltime_permanent', 'Fulltime Permanent'),
        ('fulltime_probation', 'Fulltime Probation'),
        ('part_time_contract', 'Part Time Contract'),
    )

    STATUS_CHOICES = (
        ('A', 'Active'),
        ('IN', 'Inactive'),
    )

    # Personal Details
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(
        max_length=50, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)

    # Contact Details
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=100, null=True, blank=True)

    # Employment Details
    joined_date = models.DateField(null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, null=True)
    # role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    promotion_designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, related_name='promotion', null=True, blank=True)
    manager = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICES)
    # status = models.BooleanField(default=True, null=True)
    note = models.TextField(blank=True, null=True)
    objects = ActiveEmployeeManager()

    def __str__(self):
        return f"{self.user.user_id} - {self.user.first_name}"


# Competencies Model
class Competency(models.Model):
    competency_name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    initiated_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Competencies"

    def __str__(self):
        return self.competency_name

# Onboarding Model


class Onboarding(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    onboarding_start_date = models.DateField(null=True)
    onboarding_end_date = models.DateField(null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Onboarding for Employee ID: {self.employee.id}"

# Task Model


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        # ('overdue_and_other', 'Overdue and Other'),
    )

    PRIORITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )

    title = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True)
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='pending', null=True)
    priority = models.CharField(
        max_length=100, choices=PRIORITY_CHOICES, null=True)
    approval = models.BooleanField(default=False, choices=[(
        True, 'Request Accepted'), (False, 'Request Declined')], blank=True, null=True)
    performance_rating = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    # action = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def update_status_based_on_deadline(self):
        if self.due_date < date.today():
            self.status = 'overdue'
            self.performance_rating = 0.0

    def calculate_performance_rating(self):
        if self.status == 'completed':
            print(self.status)
            if self.due_date > date.today():
                self.performance_rating = 12.0
            elif self.due_date == date.today():
                print("2")
                self.performance_rating = 10.0
            else:
                self.performance_rating = 0.0

        else:
            self.performance_rating = None

    def save(self, *args, **kwargs):
        self.calculate_performance_rating()
        self.update_status_based_on_deadline()
        print(self.calculate_performance_rating())
        super(Task, self).save(*args, **kwargs)


class Probation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    date_of_permanency = models.DateField(null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.id} - {self.employee.user.first_name}"

# Promotion/Recognition Model..myb make it models


class Promotion(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='promoted_employee')
    date_of_promotion = models.DateField(null=True)
    reason = models.CharField(max_length=100, null=True)
    note = models.TextField(blank=True, null=True)
    bonus = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    past_position = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, related_name='past_position'
    )
    new_position = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, related_name='new_position'
    )
    new_position = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, related_name='new')
    employment_type = models.CharField(
        max_length=20, choices=Employee.EMPLOYMENT_TYPE_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.employee:
            current_designation = self.employee.designation
            if self.past_position != current_designation:
                self.past_position = current_designation
            if self.new_position and self.new_position != current_designation:

                self.employee.designation = self.new_position
                self.employee.save()

        super(Promotion, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.id} - {self.employee.user.first_name} - Promoted"


# Termination Model
class Termination(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True)
    date_of_termination = models.DateField(null=True)
    reason = models.CharField(max_length=100, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.id} - {self.employee.user.first_name} - Terminated"

# Courses Model


class Course(models.Model):
    course_id = models.CharField(max_length=50, null=True)
    course_name = models.CharField(max_length=100, null=True)
    coach = models.ManyToManyField(Employee, blank=True)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_id

# Training Model


class Training(models.Model):
    training_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='courses', null=True)
    trainer = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name='trainer', null=True)
    initiated_date = models.DateTimeField(auto_now_add=True, null=True)
    participants = models.ManyToManyField(Employee)
    STATUS_CHOICES = (
        ('PA', 'Pending Approval'),
        ('S', 'Scheduled'),
        ('C', 'Completed'),
        ('CA', 'Cancelled'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return str(self.training_course)

# Development Model


class DevelopmentPlan(models.Model):
    IDP_name = models.CharField(max_length=100, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, related_name='IDP_employee', null=True)
    goal = models.ForeignKey(
        Task, on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, blank=True, null=True)
    coach = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='coach')
    initiated_date = models.DateTimeField(auto_now_add=True, null=True)
    STATUS_CHOICES = (
        ('NI', 'Not Initiated'),
        ('I', 'Initiated'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"IDP for {self.IDP_name} - {self.employee.user.first_name}"

# Appraisal Model


class Matrix(models.Model):
    POTENTIAL_CHOICES = (
        ('L', 'Low'),
        ('M', 'Moderate'),
        ('H', 'High'),
    )
    category = models.CharField(
        max_length=2, choices=POTENTIAL_CHOICES, null=True)
    note = models.CharField(max_length=100, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Matrices"

    def __str__(self):
        return self.category


class Question(models.Model):
    question_text = models.CharField(max_length=200, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.question_text


class Appraisal(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, blank=True)
    appraisal_cycle = models.CharField(
        max_length=100, null=True)  # appraisal_name
    competencies = models.ManyToManyField(Competency)
    questions = models.ManyToManyField(Question)
    potential = models.ForeignKey(
        Matrix, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    evaluators = models.ManyToManyField(Employee, related_name='evaluators')
    colleagues = models.ManyToManyField(Employee, related_name='colleagues')
    # students - but it is hard to prepare a form to be filled by a student so manager/admin ymolawal
    others = models.CharField(max_length=100, blank=True, null=True)
    start_from = models.DateTimeField(auto_now_add=True, null=True)
    to = models.DateTimeField(null=True)
    # for report ከጠቀመ እንጂ no other use
    due_date = models.DateTimeField(null=True)
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
        # ('O', 'Overdue'),
    )
    appraisal_Status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, null=True)
    final_rating = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)  # potential assessment

    def __str__(self):
        return f"{self.appraisal_cycle} - {self.appraisal_Status}"


# Report Model ....may not be necessary

# Document Model


class Document(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    file = models.FileField(upload_to='documents/', null=True)
    author = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # Employees who can view this news
    employees = models.ManyToManyField(
        Employee, related_name='documents', blank=True)

    # Managers who can view this news
    managers = models.ManyToManyField(
        Employee, related_name='manager_docs', blank=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

# News Model


class News(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    news_image = models.ImageField(
        null=True, blank=True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    publisher = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, related_name='Author', null=True)

    # Employees who can view this news
    employees = models.ManyToManyField(
        Employee, related_name='news', blank=True)

    # Managers who can view this news
    managers = models.ManyToManyField(
        Employee, related_name='manager_news', blank=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.title} - {self.publisher}"


class Notification(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, related_name='sender_notification')
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, related_name='recipient_notification')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)
