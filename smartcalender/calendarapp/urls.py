from django.urls import path
from .views import UserViewSet, SchedulerViewSet, UserRetrieveUpdateView, UserDeleteView
from rest_framework.routers import DefaultRouter
# from .views import LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'scheduler', SchedulerViewSet, basename='scheduler')



urlpatterns = [
    path('users/<int:pk>/', UserRetrieveUpdateView.as_view(), name='user-retrieve-delete'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    # path('login/', LoginView.as_view(), name='login'),
 ] + router.urls 
