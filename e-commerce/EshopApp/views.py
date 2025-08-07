import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from EshopApp.models import ORDERSTATUS, Booking, Cart, Category, ContactMessage,Product, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list,15)  

    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
    }
    return render(request, 'mainfolder/index.html', context)


#terms and conditions page function
def terms_conditions(request):
    return render(request,'mainfolder/terms_conditions.html')

#privacy and policy page function
def privacy_policy(request):
    return render(request,'mainfolder/policy-privacy.html')


def products(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category') 
    featured_products = Product.objects.filter(is_featured=True)[:6]

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': int(category_id) if category_id else None,
        'featured_products':featured_products
    }
    return render(request, 'mainfolder/products.html', context)


def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'mainfolder/admin-login.html', dic)

def adminHome(request):
    return render(request, 'admin/admin_base.html')

@login_required(login_url='admin_login') 
def admin_dashboard(request):
    # Allow access only to staff or superuser
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    
    users_count=User.objects.count()
    product_counts=Product.objects.count()
    categories_count=Category.objects.count()
    orders_count=Booking.objects.count()
    new_order = Booking.objects.filter(status=1).count()
    dispatch_order = Booking.objects.filter(status=2).count()
    way_order = Booking.objects.filter(status=3).count()
    deliver_order = Booking.objects.filter(status=4).count()
    cancel_order = Booking.objects.filter(status=5).count()
    return_order = Booking.objects.filter(status=6).count()
    recent_orders = Booking.objects.order_by('-created', '-id')[:10]
    contact_msg=ContactMessage.objects.count()
    context={
        "users_count":users_count,
        "product_counts":product_counts,
        "categories_count":categories_count,
        "orders_count":orders_count,
        "new_order":new_order,
        "dispatch_order":dispatch_order,
        "way_order":way_order,
        "deliver_order":deliver_order,
        "cancel_order":cancel_order,
        "return_order":return_order,
        "recent_orders":recent_orders,
        "contact_msg":contact_msg
    }
    return render(request, 'admin/admin_dashboard.html',context)

#Add Category
def add_category(request):
    msg = ""
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            msg = "Category added"
            return redirect('add_category')  
        else:
            msg = "Category name is required"
    return render(request, 'admin/add-category.html', locals())

#View Category
def view_category(request):
    category=Category.objects.all()
    return render(request,'admin/view_category.html',{'category':category})

#Edit Category
def update_category(request, pk):
    category=Category.objects.filter(pk=pk).first()
    if not category:
        return redirect('view_category')

    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('view_category')
        
    return render(request, 'admin/edit-category.html', {'category': category})

#delete category
def delete_category(request,pk):
    category=Category.objects.filter(pk=pk).first()
    if category:
        category.delete()
    return redirect('view_category')

#Add Product 
def add_product(request):
    category=Category.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        price=request.POST['price']
        description=request.POST['description']
        cat=request.POST['category']
        discount=request.POST['discount']
        image=request.FILES['image']
        catobj=Category.objects.get(id=cat)
        
        if not discount:
            discount = 1.0 
            
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=description, image=image)
        # messages.success(request, "Product added successfully!") 
        return redirect('add_product')  

    return render(request, 'admin/add-product.html', {'category': category})


#View Category
def view_product(request):
    product=Product.objects.all()
    return render(request,'admin/view_product.html',{'product':product})

def details_product(request,pk):
    product=Product.objects.get(pk=pk)
       
    return render(request,'admin/details-product.html',{'product':product})

# Update Product
def update_product(request, pk):
    category = Category.objects.all()
    product = Product.objects.filter(id=pk).first()

    if not product:
        return redirect('view_product')  

    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.discount = request.POST['discount']
        cat_id = request.POST['category']
        product.category = Category.objects.get(id=cat_id)

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('view_product')  

    return render(request, 'admin/update-product.html', {
        'product': product,
        'category': category
    })

def delete_product(request,pk):
    product=Product.objects.filter(pk=pk).first()
    if product:
        product.delete()
    return redirect('view_product')


def registration(request):
    context = {} 
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        image = request.FILES.get('image')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(
                username=email,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password
            )
            UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
            messages.success(request, "Registration Successful")
            return redirect('login')  # redirect after successful registration

    return render(request, 'mainfolder/register.html', context)

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'mainfolder/user-login.html', locals())

def user_profile(request):
    data, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        mobile = request.POST['mobile']

        try:
            image = request.FILES['image']
            data.image = image
        except:
            pass  # If image not uploaded, skip

        data.mobile = mobile
        data.address = address
        data.save()

        User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)

        messages.success(request, "Profile updated")
        return redirect('user_profile')

    return render(request, 'mainfolder/user-profile.html', {'data': data})


#User Logout 
def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')

#change password
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=old_password)
        if user:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'mainfolder/change-password.html')

#Product Details
def product_detail(request, pid):
    product = get_object_or_404(Product, id=pid)
    latest_products = Product.objects.exclude(id=pid).order_by('-id')[:3]
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]
    
    context = {
        'product': product,
        'latest_products': latest_products,
        'similar_products':similar_products,
    }
    
    return render(request, "mainfolder/product-details.html", context)

#add to cart
@login_required(login_url='login') 
def addToCart(request, pid):
    myli = {"objects": []}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid): 1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    context={
        'product': product,
        'lengthpro': lengthpro
    }
    return render(request, 'mainfolder/product-cart.html', context)

def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

def cart_ok(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    context={
        'product': product,
        'lengthpro': lengthpro
    }
    return render(request, 'mainfolder/cart.html', context)


@login_required(login_url='login')
def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * int(product.price)
    if request.method == "POST":
        return redirect('/payment/?total='+str(total))
    return render(request, "mainfolder/booking.html", locals()) 

#my order
def myOrder(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    order_list = []

    for booking in bookings:
        try:
            product_data = json.loads(booking.product.replace("'", '"'))['objects'][0]
        except Exception:
            product_data = {}

        items = []
        for pid, qty in product_data.items():
            try:
                prod = Product.objects.get(id=int(pid))
                items.append({
                    'name': prod.name,
                    'image': prod.image.url if prod.image else '/static/img/product.png',
                    'qty': qty,
                    'price': prod.price,
                })
            except Product.DoesNotExist:
                continue

        order_list.append({
            'id': booking.id,
            'total': booking.total,
            'created': booking.created,
            'status': booking.status,
            'items': items,
        })

    context = {
        'order': order_list,
        'orderstatus': ORDERSTATUS,
    }
    return render(request, "mainfolder/my-order.html", context)


#change order status
def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')    

def payment(request):
    total = request.GET.get('total')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'mainfolder/payment.html', locals())


#Manage Order
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'admin/manage_order.html', locals()) 

#delete order
def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

#order details
def order_detail(request, id):
    order = get_object_or_404(Booking, id=id)
    return render(request, 'admin/order_details.html', {'order': order})


#Admin Tracking Order
def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin/admin-order-track.html', locals()) 


#user manage
def manage_user(request):
    users=UserProfile.objects.all()
    context={
        'users':users
    }
    return render(request,'admin/manage-user.html',context)

#Delete User
def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 

#admin Change Password
def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin/admin_change_password.html')

#contact us function
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic validation 
        if not name or not email or not message:
            messages.error(request, "Please fill out all fields.")
        else:
            # Save message to database
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Message sent successfully.")

    return render(request, "mainfolder/contact.html")

#admin section profile
def profile(request):
    data, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        mobile = request.POST['mobile']

        try:
            image = request.FILES['image']
            data.image = image
        except:
            pass  # If image not uploaded, skip

        data.mobile = mobile
        data.address = address
        data.save()

        User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)

        messages.success(request, "Profile updated")
        return redirect('profile')

    return render(request, 'admin/profile.html', {'data': data})

