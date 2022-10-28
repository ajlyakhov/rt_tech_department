from django.forms import ModelForm

from .models import Department, Employee


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
