from django import forms
from django.contrib.auth.forms import UserCreationForm
from performance.models import *
# from django.contrib.auth.forms import AuthenticationForm

# class LoginForm(AuthenticationForm):
#     id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Employee ID'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))


class EmployeeRegistrationForm(UserCreationForm):
    is_manager = forms.BooleanField(required=False, widget=forms.Select(
        choices=[(False, 'No'), (True, 'Yes')]))
    is_employee = forms.BooleanField(required=False, widget=forms.Select(
        choices=[(False, 'No'), (True, 'Yes')]))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'user_id',
                  'is_manager', 'is_employee')

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['user_id'].widget.attrs['class'] = 'form-control'


class EmployeeForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Employee.GENDER_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=Employee.STATUS_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    note = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 40}), required=False)

    class Meta:
        model = Employee
        fields = ['avatar', 'gender', 'dob', 'nationality', 'marital_status', 'phone_number', 'email', 'address', 'joined_date', 'department', 'designation',
                  'employment_type', 'salary', 'promotion_designation', 'manager', 'status', 'note']
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'form-control'}),
            'status': forms.RadioSelect(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].empty_label = 'Select Department'
        self.fields['designation'].queryset = Designation.objects.all()
        self.fields['designation'].empty_label = 'Select Designation'
        self.fields['promotion_designation'].queryset = Designation.objects.all()
        self.fields['promotion_designation'].empty_label = 'Select Promotion Title'
        self.fields['manager'].queryset = CustomUser.objects.all()
        self.fields['manager'].empty_label = 'Select Manager'
        self.fields['marital_status'].choices = [
            ('', 'Marital Status')] + list(Employee.MARITAL_STATUS_CHOICES)
        self.fields['employment_type'].choices = [
            ('', 'Employment Type')] + list(Employee.EMPLOYMENT_TYPE_CHOICES)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': "form-control", 'placeholder': field})

        choice_fields = ['department', 'designation', 'promotion_designation',
                         'employment_type', 'manager', 'marital_status']

        for field_name in choice_fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-select'})


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ["joined_date", "department", "designation",
                   "employment_type", "salary", "promotion_designation", "manager", "created_at", "updated_at", "status", "note"]


class MyTaskForm(forms.ModelForm):
    class Meta:

        model = Task
        fields = ["status"]
