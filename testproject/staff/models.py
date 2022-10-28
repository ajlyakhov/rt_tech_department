from datetime import date

from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
            

class Employee(models.Model):
    class Meta:
        indexes = [
                models.Index(fields=['surname'])
                ]

    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    photo = models.ImageField()
    position = models.CharField(max_length=50)
    salary = models.IntegerField()
    birth_date = models.DateField()
    department = models.ForeignKey(Department, related_name='employee', on_delete=models.PROTECT)
    is_chief = models.BooleanField(default=False)

    @property
    def age(self):
        today = date.today()
        years = today.year - self.birth_date.year
        if today.month < self.birth_date.month:
            years -= 1
        elif today.month == self.birth_date.month and today.day < self.birth_date.day:
            years -= 1
        return years

    def save(self, *args, **kwargs):
        if self.is_chief:
            self.__class__.objects.filter(department=self.department, is_chief=True)\
                    .update(is_chief=False)
        super().save(*args, **kwargs)
