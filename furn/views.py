from django.shortcuts import render, redirect, get_object_or_404
from . models import Blog, Product, Contact, OrderItem, Orders, Address, Payment
from . forms import ProfileForm, SignupForm, AddressForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
import random
import string
import stripe
# Create your views here.
stripe.api_key = "sk_test_26PHem9AhJZvU623DfE1x4sd"

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def home(request):
    products = Product.objects.all()[:3]
    blogs = Blog.objects.all()[:5]

    context = {"products": products, "blogs": blogs}
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html")

def blogs(request):
    blogs = Blog.objects.all()
    context = {"blogs": blogs}
    return render(request, "blog.html", context)

def products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "shop.html", context)

def product(request, slug):
    product = Product.objects.get(slug=slug)
    context = {"product": product}
    return render(request, "product.html", context)

def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(first_name=first_name, last_name=last_name, email=email, message=message)
        contact.save()
        
        messages.success(request, 'Your message was received. We will get back to you shortly')
        return redirect("home")
    return render(request, "contact.html") 
    
def register(request):
    form = SignupForm()
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect("home")
    context = {"form": form}
    return render(request, "register.html", context)

@login_required(login_url='login')
def profile(request, username):
    user = User.objects.get(username= request.user)
    form = ProfileForm(instance=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=form)
        if form.is_valid():
            f0rm.save()
            return redirect("home")
    context ={"user": user, "form": form}
    return render(request, "profile.html", context)

def orders(request, username):
    user = User.objects.get(username= request.user)
    orders = Orders.objects.filter(user=user, ordered=True)
    order= Orders.objects.filter(orderItem__user=user, ordered=True)
    context={"orders":orders, "order": order}
    return render(request, "orders.html", context)


def edit_profile(request, username):
    user = User.objects.get(username= request.user)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile was updated.")
            return redirect("profile", username=request.user)
    context ={"form": form}
    return render(request, "edit_profile.html", context)

@login_required(login_url='login')
def cart(request, user):
    cart = OrderItem.objects.filter(user=request.user, ordered=False)
    total = 0
    for i in cart:
        quantity = i.quantity
        price = i.product.price
        prant = quantity * price
        total = total + prant
    context ={"cart": cart, "total": total}
    return render(request, "cart.html", context)

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart, created = OrderItem.objects.get_or_create(product=item, user=request.user, ordered=False)
    order_qs = Orders.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.orderItem.filter(product__slug=item.slug).exists():
            cart.quantity += 1
            cart.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart", user=request.user)
    
        else:
            order.orderItem.add(cart)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart", user=request.user)
        
    else:
        order_date = timezone.now()
        order = Orders.objects.create(
            user=request.user, order_date=order_date)
        order.orderItem.add(cart)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart", user=request.user)
    

def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orders.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs
        # check if the order item is in the order
        if order.orderItem.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )
            order.orderItem.remove(orderItem)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart", user=request.user)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart", user=request.user)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart", user=request.user)


def add_quantity(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orders.objects.filter(orderItem__product=item, user=request.user, ordered=False)
    cart = OrderItem.objects.get(product=item, user=request.user, ordered=False)
    if order_qs.exists():
        cart.quantity += 1
        cart.save()
    messages.info(request, "The item quantity was updated.")
    return redirect("cart", user=request.user)
    

def reduce_quantity(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orders.objects.filter(orderItem__product=item, user=request.user, ordered=False)
    cart = OrderItem.objects.get(product=item, user=request.user, ordered=False)
    if order_qs.exists():
        cart.quantity -= 1
        cart.save()
        messages.info(request, "The item quantity was updated.")
    else:
        cart.delete()
        messages.info(request, "This item was removed from your cart.")
    
    return redirect("cart", user=request.user)


class CheckOutView(View):
    def get(self, request, *args, **kwargs):
        
        try:
            order = Orders.objects.get(user=self.request.user, ordered=False)
            orders = OrderItem.objects.filter(user=self.request.user, ordered=False)
            address_qs= Address.objects.filter(user=self.request.user)
            if not address_qs.exists():
                form = AddressForm()
            else:
                user_address=Address.objects.get(user=self.request.user)
                form = AddressForm(instance=user_address)

            total = 0
            for i in orders:
                quantity = i.quantity
                price = i.product.price
                prant = quantity * price
                total = total + prant
            
            context= {"order": order, "form": form, "orders": orders, "total": total}
            
            
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(request, "You don't have an active order.")
            return redirect("cart", user=request.user)
        
    def post(self, request, *args, **kwargs):
        try:
            address_qs = Address.objects.filter(user=self.request.user)
            order = Orders.objects.get(user=self.request.user, ordered=False)
            if request.method == 'POST':
                if not address_qs.exists():
                    form = AddressForm(self.request.POST)

                else:
                    user_address=Address.objects.get(user=self.request.user)
                    form = AddressForm(self.request.POST, instance=user_address)

                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = self.request.user
                    obj.save()
                    address = address_qs[0]
                    order.address = address
                    order.save()
                    return redirect("payment")
        except Exception as e:
            print(e)
        except ObjectDoesNotExist:
            messages.info(request, "You don't have an active order.")
            return redirect("checkout")

        return redirect("home")

class PaymentView(View):
    def get(self, request, *args, **kwargs):
        order = Orders.objects.get(user=self.request.user, ordered=False)
        user = User.objects.get(username=request.user)
        context = {"order": order}
        return render(self.request, "payment.html", context)

    def post(self, request, *args, **kwargs):
        order = Orders.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total() * 100)
        customer=stripe.Customer.create(
            name=request.user,
            )
        if request.method == 'POST':
            card_number= request.POST['card_number']
            card_exp_month= request.POST['card_exp_month']
            card_exp_year= request.POST['card_exp_year']
            card_cvc= request.POST['card_cvc']
            card_t=stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": card_exp_month,
                "exp_year": card_exp_year,
                "cvc": card_cvc,
            },
            )
           
            
            card_created=stripe.Customer.create_source(
                customer.id,
            source=card_t,
            )
        try:
            charge=stripe.PaymentIntent.create(
                payment_method_types=["card"],
                amount=amount,
                currency="usd",
                customer=customer,
                payment_method=card_created,
            )
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_items = order.orderItem.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.ref_number = create_ref_code()
            order.save()

            return redirect("thank-you")
        except Exception as e:
            print(e)
    
        return redirect("thank-you")
    

def thank_you(request):
    return render(request, "thankyou.html")






