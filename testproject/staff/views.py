from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Department, Employee
from .forms import DepartmentForm, EmployeeForm


class DepartmentView(FormView, ListView):
    model = Department
    template_name = 'staff/department_form.html'
    form_class = DepartmentForm
    success_url = reverse_lazy('department')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DepartmentUpdateView(DepartmentView, UpdateView):

    def post(self , request , *args , **kwargs):
        self.object = self.get_object()
        return super().post(request , *args , **kwargs)


class DepartmentDeleteView(DepartmentView, DeleteView):

    def post(self , request , *args , **kwargs):
        self.object = self.get_object()
        return super().post(request , *args , **kwargs)


class EmployeeView(FormView, ListView):
    model = Employee
    template_name = 'staff/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee')
    
    def post(self , request , *args , **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request , *args , **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmployeeUpdateView(EmployeeView, UpdateView):
    
    def post(self , request , *args , **kwargs):
        self.object = self.get_object()
        return super().post(request , *args , **kwargs)



class EmployeeDeleteView(EmployeeView, DeleteView):
    
    def post(self , request , *args , **kwargs):
        self.object = self.get_object()
        return super().post(request , *args , **kwargs)

