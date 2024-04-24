from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views.generic import TemplateView , View , CreateView , FormView
from .models import *
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .forms import CustomerRegistrationForm, CustomerLoginForm
from django.contrib.auth import authenticate, login, logout 
from django.db.models import Q
from django.core.paginator import Paginator
import json
import requests




class storeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

class HomeView(storeMixin,TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #kwargs is a dictionary of all the arguments passed to the view it is used to pass additional data to the template
        all_products = Product.objects.order_by("-id")
        paginator = Paginator(all_products, 7) 
        page_number = self.request.GET.get("page")
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class GroceryView(storeMixin,TemplateView):
    template_name = "groceries.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="Groceries").product_set.all()
        return context
    
class SnacksView(storeMixin,TemplateView):
    template_name = "snacks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="Snacks").product_set.all()
        return context
    
class BeveragesView(storeMixin,TemplateView):
    template_name = "beverages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="Beverages").product_set.all()
        return context

class HomecareView(storeMixin,TemplateView):
    template_name = "personalandhomecare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="Personal care and hygiene").product_set.all()
        return context

class PackagedfoodsView(storeMixin,TemplateView):
    template_name = "packagedfoods.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="packaged food").product_set.all()
        return context

class StationariesView(storeMixin,TemplateView):
    template_name = "stationaries.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="stationary").product_set.all()
        return context

class OthersView(storeMixin,TemplateView):
    template_name = "others.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Category.objects.get(title="others").product_set.all()
        return context
    
class ProductDetailView(storeMixin,TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs['slug']
        context['product'] = Product.objects.get(slug=slug)
        
        return context

class AddToCartView(storeMixin,TemplateView):  
    

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from url
        pro_id = kwargs['pro_id']

        #get product
        product_obj = Product.objects.get(id=pro_id)
        #check if cart exists
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj =Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    rate=product_obj.price,
                    quantity=1,
                    subtotal=product_obj.price
                )
                cart_obj.total = Decimal(cart_obj.total)
                cart_obj.total += product_obj.price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(cart_id=1)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj,
                product=product_obj,
                rate=product_obj.price,
                quantity=1,
                subtotal=product_obj.price
            )
            cart_obj.total = Decimal(cart_obj.total)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return redirect(reverse("store:mycart"))
    
class MyCartView(storeMixin,TemplateView):
    template_name = "mycart.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
    
class ManageCartView(storeMixin,View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect(reverse("store:mycart"))
    
class EmptyCartView(storeMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect(reverse("store:mycart"))
    
class CheckoutView(storeMixin,TemplateView):
    template_name = "checkout.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.customer:
            return super().dispatch(request, *args, **kwargs)
        else:
            #after login user will be redirected to checkout page
            return redirect(reverse("store:customerlogin") + "?next=/checkout/")

            

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

    # get detail from the form and save it to the database
    def post(self, request, *args, **kwargs):
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        
        order = Order.objects.create(
            cart=cart,
            name=name,
            email=email,
            phone=phone,
            address=address,
            total=cart.total,
            order_id=cart.cart_id
            
        )
        del request.session['cart_id']
        return redirect(reverse("store:paymentmethod")+ "?o_id=" + str(order.id)) 
    
class PaymentMethodView(storeMixin,TemplateView):
    template_name = "paymentmethod.html"

    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get("o_id")
        order = Order.objects.get(id=order_id)
        context['order'] = order
        return context
    
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        amount = request.POST.get("amount")
        #convert amount to paisa
        amount_new = int(float(amount)*100)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        url ="https://a.khalti.com/api/v2/epayment/initiate/"
        
        payload = json.dumps(
        {
            "return_url": "http://127.0.0.1:8000/verify-payment/",
            "website_url": "http://127.0.0.1:8000/",
            "amount": amount_new,
            "purchase_order_id": order_id,
            "purchase_order_name": "E-pasal",
            "customer_info": {
            "name": name,
            "email": email,
            "phone": phone
            }
        })
        headers = {
            'Authorization': 'key f0755fada7f54733b7e2627ee275e91a',
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        if response.status_code == 200:
            payment_url = response.json().get("payment_url")
            return redirect(payment_url)
        else:   
            return redirect(reverse("store:paymentmethod") + "?o_id=" + order_id)
        

def verify_payment(request):

    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key f0755fada7f54733b7e2627ee275e91a',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            order = Order.objects.get(id=order_id)
            order.payment_method = "Khalti"
            order.save()

            return redirect(reverse("store:paymentsuccess"))
            
        else:
            return redirect(reverse("store:paymentfailed"))
        
class PaymentSuccessView(storeMixin,TemplateView):
    template_name = "paymentsuccess.html"

class PaymentFailedView(storeMixin,TemplateView):
    template_name = "paymentfailed.html"
            
       


        
    
    

        
        
    

    



    

class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        
        email = form.cleaned_data.get("email")

        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)

        return super().form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return self.success_url
    
class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("store:home"))
    
class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = "/"

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form":form, "error":"Invalid Credentials"})

        
        return super().form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return self.success_url



class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.customer:
            return super().dispatch(request, *args, **kwargs)
        else:
            #after login user will be redirected to checkout page
            return redirect(reverse("store:customerlogin") + "?next=/profile/")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context['orders'] = orders

        return context

   
class CancelOrderView(View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['cp_id']
        order = Order.objects.get(id=order_id)
        order.status = "Order Cancelled"
        order.save()
        return redirect(reverse("store:customerprofile"))
    

class CustomerOrderDetailView(TemplateView):
    template_name = "orderdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['cp_id']
        order = Order.objects.get(id=order_id)
        context['order'] = order
        return context
        

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(name__contains=kw) | Q(description__contains=kw))
        context['results'] = results
        return context




        
    
    

    
    
