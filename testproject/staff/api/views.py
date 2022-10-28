from django.conf import settings
from django.db.models import Count, Sum
from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from staff.models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeReadSerializer, EmployeeWriteSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department
    queryset = Department.objects.prefetch_related('employee')\
            .annotate(salary_sum=Sum('employee__salary'),
                      salary_count=Count('employee__salary'))
    serializer_class = DepartmentSerializer
    pagination_class = None


class EmployeeViewSet(viewsets.ModelViewSet):
    model = Employee
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['surname', 'department']
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return EmployeeWriteSerializer

        return EmployeeReadSerializer
