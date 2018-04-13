# Create your views here.
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, DetailView, CreateView
from django.db.models import Q
from .models import Customers,Subscription,Product


class CustomerSearchView(TemplateView):
    template_name = 'crm/customers_list.html'
    model = Customers
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super(CustomerSearchView, self).get_context_data(**kwargs)

        #Get search parameeters
        if self.request.GET.get("phone_mail_query"):
            customers = CustomerSearchView.search_customers_by_mail(self.request.GET.get("phone_mail_query"))
        elif self.request.GET.get("zipcode_query"):
            customers = CustomerSearchView.search_customers_by_adress(self.request.GET.get("zipcode_query"),
                                                                      self.request.GET.get("house_query"))
        else:
            customers = Customers.objects.all()
        context.update({"objects": customers})
        return context

    @staticmethod
    def search_customers_by_mail(q):
        q = Q(email__icontains=q) | Q(phone__icontains=q)
        return Customers.objects.filter(q).distinct()

    @staticmethod
    def search_customers_by_adress(zip_query,house_query):
        q = Q(address__zip_code__icontains=zip_query) and Q(address__house_number__icontains=house_query)
        return Customers.objects.filter(q).distinct()


class CustomerDetailView(DetailView):
    template_name = 'crm/customer_details.html'
    model = Customers

    def dispatch(self, *args, **kwargs):
        return super(CustomerDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        customer_subscriptions = Subscription.objects.filter(customer__id=self.kwargs['pk'])
        available_products = Product.objects.all()
        context.update({'subscriptions': customer_subscriptions,
                        'products': available_products})

        return context

    def post(self, request, *args, **kwargs):
        selected_product = request.POST.get('choice','')
        if selected_product:
            with transaction.atomic():
                Subscription.objects.create(
                    customer=Customers.objects.get(pk=self.kwargs['pk']),
                    product=Product.objects.get(pk=selected_product),
                    expiry_date=datetime.now(),
                    balance=45
                )
        return HttpResponseRedirect(reverse('customers_detail', kwargs={'pk': self.kwargs['pk']}))


class CustomerCreateView(CreateView):
    template_name = 'crm/customers_create.html'
    model = Customers
    fields = ('__all__')

    def form_valid(self, form):
        customer = form.save()
        customer.save()
        return HttpResponseRedirect(reverse('customers_detail', kwargs={'pk': customer.id}))