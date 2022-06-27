from django.urls import path
from . import views

app_name = 'carservice'

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('cars/<int:pk>', views.CarDetail.as_view(), name='car-detail'),
    path('orders/', views.RepairOrderView.as_view(), name='order-list'),
    path('services/', views.ServicesView.as_view(), name='service-list'),
    path('orders/<int:pk>', views.OrderDetail.as_view(), name='order-detail'),
    path('create_order/', views.CarRepairOrder.as_view(), name='create-order'),
]