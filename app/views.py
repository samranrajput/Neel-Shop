from django.shortcuts import render,redirect
from .models import Product, Customer, Cart, OrderPlaced, Wishlist
from .forms import CustomerSignUp, ProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from ec import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives

@login_required
def home(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    return render(request, 'home.html', locals())

@login_required
def about(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())

        total_cart = len(Cart.objects.filter(user=request.user))
    return render(request, 'about.html', locals())

@login_required
def contact(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())

        total_cart = len(Cart.objects.filter(user=request.user))
    return render(request, 'contact.html', locals())

@login_required
def category(request,val):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request,'category.html',locals())

@login_required
def categoryTitle(request,val):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values('title')
    return render(request,'category.html',locals())

@login_required
def productDetail(request,id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:
        exist_cart = Cart.objects.filter(Q(product=product) & Q(user = request.user)).exists() 
        wishlist = Wishlist.objects.filter(Q(product = product) & Q(user = request.user))
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    return render(request,'product_detail.html',locals())

def customerSignUp(request):
    form = CustomerSignUp()
    if request.method == 'POST':
        form = CustomerSignUp(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! User Register Successfully')
            return redirect('login')
        else:
            messages.warning(request,'Invalid Input Data')
    return render(request,'sign_up.html',locals())

@login_required
def profile(request):
    form = ProfileForm()
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            profile_picture = form.cleaned_data['profile_picture']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zip_code = form.cleaned_data['zip_code']
            state = form.cleaned_data['state']
            reg = Customer(user=request.user,name=name,profile_picture=profile_picture,locality=locality,city=city,mobile=mobile,zip_code=zip_code,state=state)
            reg.save()
            messages.success(request,'Congratulations! Profile Save Successfully')
            return redirect('profile')
        else:
            messages.warning(request,'Invalid Input Data')
    return render(request, 'profile.html',locals())

@login_required
def address(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    messages.success(request,'Congratulations! Profile Save Successfully')
    return render(request, 'address.html',locals())

@login_required
def updateAddress(request,id):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())

        total_cart = len(Cart.objects.filter(user=request.user))
    update_address = Customer.objects.get(id=id)
    form = ProfileForm(instance=update_address)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = update_address)
        if form.is_valid():
            form.save()
            return redirect('address')
        else:
            messages.warning(request,'Invalid Input Data')

def custom_logout_view(request):
    logout(request)
    return redirect('login')     

def addToCart(request):
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    exist_cart = Cart.objects.filter(Q(product=product) & Q(user = request.user)).exists() 
    if not exist_cart:
        Cart(user=request.user, product=product).save()
    return redirect('show_cart')

@login_required
def showCart(request):
    cart = Cart.objects.filter(user=request.user)
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'add_to_cart.html', locals())

@login_required
def checkOut(request):
    if request.method == 'GET':
        wishlist_total = len(Wishlist.objects.all())
        add = Customer.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        total_cart = len(cart_items)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40  # Adding shipping cost or any other fee

    elif request.method == 'POST':
        # Handle order creation when the form is submitted (payment button clicked)
        shipping_address_id = request.POST.get('custid')  # Get selected shipping address ID
        shipping_address = Customer.objects.get(id=shipping_address_id)

        # Loop through cart items and create order records
        cart_items = Cart.objects.filter(user=request.user)
        order_total = 0  # To calculate total price

        # Collecting order details to send in email
        order_details = []
        
        for item in cart_items:
            order = OrderPlaced.objects.create(
                user=request.user,
                customer=shipping_address,
                product=item.product,
                quantity=item.quantity,
                status='Pending',  # Initial status
                payment=None,  # Set payment to None initially
            )
            order_total += item.quantity * item.product.discounted_price
            order_details.append({
                'product': item.product.title,
                'quantity': item.quantity,
                'price': item.product.discounted_price,
                'total': item.quantity * item.product.discounted_price,
            })

        # Sending email
        try:
            subject = f"New Order from {request.user.username}"
            admin_email = "admin@example.com"  # Replace with actual admin email
            html_content = render_to_string('admin_order_notification_email.html', {
                'user': request.user,
                'order_details': order_details,
                'total_amount': order_total + 40,
            })
            
            email = EmailMultiAlternatives(
                subject=subject,
                body="Your order details are attached below.",
                from_email=settings.EMAIL_HOST_USER,
                to=[admin_email]
            )
            email.attach_alternative(html_content, "text/html")  # Attach HTML content
            email.send()

            messages.success(request, "Your order has been placed successfully!")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        # Optionally clear the cart after order is placed
        Cart.objects.filter(user=request.user).delete()

        return redirect('orders')  # Redirect to orders page or confirmation page
    
    return render(request, 'check_out.html', locals())

    
@login_required
def order(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.all()
    return render(request, 'orders.html', locals())

def wishlist(request):
    if request.user.is_authenticated:
        wishlist_total = len(Wishlist.objects.all())
        total_cart = len(Cart.objects.filter(user=request.user))
    wishlist = Wishlist.objects.all()
    return render(request, 'wishlist.html',locals())

def plusCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    
def minusCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    
def removeCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # exist_cart = Cart.objects.filter(Q(product=prod_id) & Q(user = request.user)).exists() 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # if exist_cart:
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    
def plusWishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data = {
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
def minusWishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data = {
            'message':'Wishlist remove Successfully',
        }
        return JsonResponse(data)

def search(request):
    query = request.GET['search']
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_cart = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains = query))
    return render(request, "search.html", locals())