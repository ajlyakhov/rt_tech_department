from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, EmployeeViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = router.urls

