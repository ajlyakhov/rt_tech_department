from datetime import date
from PIL import Image

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import BytesIO
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, RequestsClient
from rest_framework.authtoken.models import Token
from staff.models import Department, Employee

UserModel = get_user_model()

class StaffAPITests(APITestCase):

    def create_user(self, username, password):
        user = UserModel.objects.create_user(
            username=username,
            password=password,
        )
        return user

    def authorization(self):
        user = self.create_user('uname', 'passwors')
        token, created = Token.objects.get_or_create(user=user)
        return token

    def create_image(self, filename):
            image = BytesIO()
            Image.new('RGB', (100, 100)).save(image, 'JPEG')
            image.seek(0)

            return SimpleUploadedFile(filename, image.getvalue())
            
    def create_department(self, name):
        url = reverse('api:department-list')
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def create_employee(self, data):
        url = reverse('api:employee-list')
        photo_filename = data.pop('photo_filename')
        data['photo'] = self.create_image(photo_filename)
        response = self.client.post(url, data, format='multipart')
        return response

    def test_create_department(self):
        response = self.create_department('NewDepartment')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().name, 'NewDepartment')

    def test_create_employee(self):
        response = self.create_department('NewDepartment')
        department_id = response.data['id']
        today = date.today()
        birth_date = date(today.year - 32, 1, 1)
        new_employee_data = {
                'surname': 'Surname1',
                'name': 'Name1',
                'patronymic': 'Patronymic1',
                'photo_filename': 'photo1.jpeg',
                'position': 'Position1',
                'salary': 100000,
                'department': department_id,
                'birth_date': birth_date,
                'is_chief': True,
                }
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.create_employee(new_employee_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee_id = response.data['id']
        url = reverse('api:employee-detail', args=[employee_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], employee_id)
        self.assertEqual(response.data['surname'], 'Surname1')
        self.assertEqual(response.data['name'], 'Name1')
        self.assertEqual(response.data['patronymic'], 'Patronymic1')
        self.assertEqual(response.data['position'], 'Position1')
        self.assertEqual(response.data['salary'], 100000)
        self.assertEqual(response.data['age'], 32)
        self.assertEqual(response.data['is_chief'], True)

    def test_delete_employee(self):
        response = self.create_department('NewDepartment')
        department_id = response.data['id']
        new_employee_data = {
                'surname': 'Surname1',
                'name': 'Name1',
                'patronymic': 'Patronymic',
                'photo_filename': 'photo1.jpeg',
                'position': 'Position1',
                'salary': '100000',
                'department': department_id,
                'birth_date': date(1980, 4, 1),
                'is_chief': True,
                }
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.create_employee(new_employee_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee_id = response.data['id']
        url = reverse('api:employee-detail', args=[employee_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], employee_id)

        url = reverse('api:employee-detail', args=[employee_id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('api:employee-detail', args=[employee_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def create_structure(self):
        for_test_data = {}
        for dep in range(5):
            dep_resp = self.create_department(f'Department_{dep}')
            dep_id = dep_resp.data['id']
            salary_sum = 0
            salary_count = 0
            for emp in range(10):
                emp_data = {
                'surname': f'Surname_{dep}_{emp}',
                'name': f'Name_{dep}_{emp}',
                'patronymic': f'Patronymic_{dep}_{emp}',
                'photo_filename': f'photo_{dep}_{emp}.jpeg',
                'position': f'Position_{dep}_{emp}',
                'salary': 100000 + 10000*dep + 1000*(10-emp),
                'department': dep_id,
                'birth_date': date(1970+emp, 4, 1+dep),
                'is_chief': emp==0,
                        }
                salary_sum += 100000 + 10000*dep + 1000*(10-emp)
                salary_count += 1
                emp_resp = self.create_employee(emp_data)
            for_test_data[dep_id] = {
                    'name': f'Department_{dep}',
                    'salary_sum': salary_sum,
                    'salary_count': salary_count,
                    }
        return for_test_data

    def test_department_list(self):
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        for_test_data = self.create_structure()
        url = reverse('api:department-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for dep_result in response.data:
            dep_id = dep_result['id']
            self.assertEqual(dep_result['name'], for_test_data[dep_id]['name'])
            self.assertEqual(dep_result['salary_count'], for_test_data[dep_id]['salary_count'])
            self.assertEqual(dep_result['salary_sum'], for_test_data[dep_id]['salary_sum'])

    def test_all_employee_list(self):
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        for_test_data = self.create_structure()
        url = reverse('api:employee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 50)

    def test_employee_filter_by_department(self):
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        for_test_data = self.create_structure()
        url = reverse('api:employee-list') + '?department={}'.format(for_test_data.popitem()[0])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)

    def test_employee_filter_by_surname(self):
        token = self.authorization()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        for_test_data = self.create_structure()
        url = reverse('api:employee-list') + '?surname=Surname_1_1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

