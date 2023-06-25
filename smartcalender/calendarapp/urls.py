from django.urls import path
from .views import UserViewSet, SchedulerViewSet, UserRetrieveUpdateDeleteView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'scheduler', SchedulerViewSet, basename='scheduler')



urlpatterns = [
    path('users/<int:pk>/', UserRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-delete'),
 ] + router.urls 
