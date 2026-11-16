from django.urls import path, include
from .views import JobViewSet
from rest_framework.routers import SimpleRouter

app_name = 'jobs'
router = SimpleRouter()
router.register(r'jobs', JobViewSet, basename='jobs')


urlpatterns = [
  path('', include(router.urls)),
]