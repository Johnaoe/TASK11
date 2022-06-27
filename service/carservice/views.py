from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from .models import Car, RepairOrder, Service, Owner
from .forms import OrderForm

# Create your views here.

def index(request):
    num_cars = Car.objects.count()
    num_repair_orders = RepairOrder.objects.count()
    num_services = Service.objects.count()
    num_visits = int(request.session.get('num_visits', 0)) + 1
    request.session['num_visits'] = num_visits

    context = {
        'num_cars': num_cars,
        'num_repair_orders': num_repair_orders,
        'num_services': num_services,
        'num_visits': num_visits,

    }
    return render(request, 'carservice/index.html', context=context)

class CarListView(generic.ListView):
    model = Car
    template_name = 'carservice/car_list.html'
    context_object_name = 'cars'
    queryset = Car.objects.all()
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'debug': settings.TIME_ZONE})
        return context

class CarDetail(generic.DetailView):
    model = Car
    template_name = 'carservice/car_detail.html'
    context_object_name = 'car'

class RepairOrderView(generic.ListView):
    model = RepairOrder
    template_name = 'carservice/order_list.html'
    context_object_name = 'orders'
    queryset = RepairOrder.objects.all()
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'debug': settings.TIME_ZONE})
        return context 
    
class ServicesView(generic.ListView):
    model = Service
    template_name = 'carservice/service_list.html'
    context_object_name = 'services'
    queryset = Service.objects.all()
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'debug': settings.TIME_ZONE})
        return context

class OrderDetail(generic.DetailView):
    model = RepairOrder
    template_name = 'carservice/order_detail.html'
    context_object_name = 'order'

class CarRepairOrder(generic.CreateView):
    model = RepairOrder
    # fields = ['car', 'description']
    success_url = reverse_lazy('carservice:cars')
    template_name = 'carservice/create_order.html'
    form_class = OrderForm

class Owner(generic.DetailView):
    model = Owner
    template_name = 'carservice/order_detail.html'
    queryset = Service.objects.all()
    context_object_name = 'owner'