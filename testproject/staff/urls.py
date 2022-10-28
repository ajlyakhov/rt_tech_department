from django.urls import path

from .views import (DepartmentView, DepartmentUpdateView,  DepartmentDeleteView, 
        EmployeeView, EmployeeUpdateView, EmployeeDeleteView)

urlpatterns = [
        path('department/', DepartmentView.as_view(), name='department'),
        path('department/<int:pk>/', DepartmentUpdateView.as_view(), name='department-detail'),
        path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(),
            name='department-delete'),
        path('employee/', EmployeeView.as_view(), name='employee'),
        path('employee/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-detail'),
        path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
        ]
