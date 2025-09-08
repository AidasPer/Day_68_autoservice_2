from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name="cars"),
    path('cars/<int:car_id>', views.car, name="car"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
    path('userinstance/', views.UserOrderInstanceListView.as_view(), name='user_instance'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('instances/create', views.OrderInstanceCreateView.as_view(), name='instances_create'),
]
