from rest_framework import serializers
from staff.models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'salary_sum', 'salary_count']

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    salary_count = serializers.IntegerField(required=False)
    salary_sum = serializers.IntegerField(required=False)


class EmployeeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'surname', 'name', 'patronymic', 'photo',
                  'position', 'salary', 'age', 'department', 'is_chief']

    id = serializers.IntegerField()
    surname = serializers.CharField()
    name = serializers.CharField()
    patronymic = serializers.CharField()
    photo = serializers.ImageField()
    position = serializers.CharField()
    salary = serializers.IntegerField()
    age = serializers.IntegerField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    is_chief = serializers.BooleanField(default=False)


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'surname', 'name', 'patronymic', 'photo',
                  'position', 'salary', 'birth_date', 'department', 'is_chief']

    #id = serializers.IntegerField()
    surname = serializers.CharField()
    name = serializers.CharField()
    patronymic = serializers.CharField()
    photo = serializers.ImageField()
    position = serializers.CharField()
    salary = serializers.IntegerField()
    birth_date = serializers.DateField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    is_chief = serializers.BooleanField(default=False)
