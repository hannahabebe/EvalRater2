# forms.py

from django import forms
from .models import Employee, Promotion, Department, Course, Competency, Termination


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department', 'designation', 'employment_type',
                  'salary', 'promotion_designation', 'manager', 'status', 'note']


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        exclude = ['past_position']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class CompetencyForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = "__all__"


class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = "__all__"
