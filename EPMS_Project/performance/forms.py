# forms.py

from django import forms
from .models import *


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['avatar', 'department', 'designation', 'employment_type',
                  'salary', 'promotion_designation', 'manager', 'status', 'note']


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        # fields = "__all__"
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


class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        exclude = ["employee", "department", "designation",
                   "colleagues", "to", "others", 'appraisal_Status', 'final_rating', 'potential']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ["publisher"]


class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ["author"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class DevelopmentPlanForm(forms.ModelForm):
    class Meta:
        model = DevelopmentPlan
        exclude = ['employee']


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
