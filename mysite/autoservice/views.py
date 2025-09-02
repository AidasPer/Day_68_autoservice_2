from django.shortcuts import render, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Service, Order, Car
from .forms import OrderReviewForm

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status__exact='f').count(),
        "num_cars": Car.objects.count(),
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=context)

def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)

    return render(request, template_name="cars.html", context={'cars': paged_cars})

def car(request, car_id):
    return render(request, template_name="car.html", context={'car': Car.objects.get(pk=car_id)})

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = 'orders'
    paginate_by = 3


class OrderDetailView(FormMixin,generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = 'order'
    form_class = OrderReviewForm
    # success_url = reverse_lazy('orders')

    def get_success_url(self):
        return reverse('order', kwargs={"pk": self.get_object().pk})




    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.order = self.get_object()
        form.save()
        return super().form_valid(form)

def search(request):
    query = request.GET.get('query')
    context = {
        'query': query,
        'cars': Car.objects.filter(Q(make__icontains=query) | Q(client_name__icontains=query) | Q(model__icontains=query) | Q(license_plate__icontains=query) | Q(vin_code__icontains=query))
    }
    return render(request, template_name='search.html', context=context)

class UserOrderInstanceListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_instances.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('index')