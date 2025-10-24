from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('counters/', views.get_counters, name='get_counters'),
    path('counters/create/', views.create_counter_endpoint, name='create_counter'),
    path('counters/<int:counter_id>/update/', views.update_counter_endpoint, name='update_counter'),
    path('counters/<int:counter_id>/delete/', views.delete_counter_endpoint, name='delete_counter'),
    path('counters/reset/', views.reset_counters_endpoint, name='reset_counters'),
    # Category management endpoints
    path('counters/<int:counter_id>/categories/', views.assign_categories_endpoint, name='assign_categories'),
    path('counters/<int:counter_id>/categories/get/', views.get_categories_endpoint, name='get_categories'),
    path('categories/all/', views.get_all_categories_endpoint, name='get_all_categories'),
]
