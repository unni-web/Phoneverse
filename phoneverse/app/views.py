from django.shortcuts import render,redirect,redirect,get_list_or_404,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . models import *
from django.contrib import messages


# Create your views here.
def adminlogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='admin' and password=='admin':
        return redirect(adminpage)
        
    return render(request, 'adminlogin.html')


def adminpage(request):
    return render(request, 'adminpage.html')

def addproduct(request):
    if request.method=='POST':
        name=request.POST['name']
        category=request.POST['category']
        description=request.POST['description']
        phone_price=request.POST['phone_price']
        phone_image = request.FILES.get('phone_image')
        data=phonedetails.objects.create(name=name,category=category,description=description,phone_price=phone_price,phone_image=phone_image)
        print (data)
        data.save()
        return redirect (viewproduct)
        
    return render(request, 'addproduct.html')

def viewproduct(request):
    products = phonedetails.objects.all()
    return render(request, 'viewproduct.html', {'products': products})

def viewproductupdate(request,pk):
    product=get_list_or_404(phonedetails,pk=pk)
    if request.method==['POST']:
        product.name=request.POST['name']
        product.category=request.POST['category']
        product.description=request.POST['description']
        product.phone_price=request.POST['phone_price']
        
    return render(request ,'')



def viewproductdelet(request,pk):
    phonedetails.objects.get(pk=pk).delete()

    return redirect(viewproduct)


def category_view(request, category):
    phones = phonedetails.objects.filter(category=category.lower())
    context = {
        'category': category,
        'phones': phones
    }
    return render(request, 'iphone.html', context)

def category_view_samsung(request, category):
    phones = phonedetails.objects.filter(category=category.lower())
    context = {
        'category': category,
        'phones': phones
    }
    return render(request, 'samsung.html', context)

def category_view_pixel(request, category):
    phones = phonedetails.objects.filter(category=category.lower())
    context = {
        'category': category,
        'phones': phones
    }
    return render(request, 'pixel.html', context)

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cnf_password=request.POST['cnf_password']
        if cnf_password==password:
            data=User.objects.create_user(username=username,email=email,password=password)
            data.save()
            return redirect(loginuser)
    return render(request,'register.html')

def loginuser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)  
            return redirect(index)
        else:
            return redirect(loginuser)      

    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect(loginuser)

def index(request):
    if request.user.is_authenticated:
        products = phonedetails.objects.all()
        
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()

        cart_total = 0
        for item in cart_items:
            cart_total += item.product.phone_price * item.quantity

        return render(
            request,
            'index.html',
            {
                'products': products,
                'cart_count': cart_count,
                'cart_total': cart_total
            }
        )

    else:
        return redirect(loginuser)


def iphone(request):
    return render(request,'iphone.html')

def samsung(request):
    return render(request,'samsung.html')

def pixel(request):
    return render(request,'pixel.html')

def account(request):
    return render(request,'account.html')

# def cart(request,id):
#     return render(request,'cart.html')


def addtocart(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first")
        return redirect('loginuser')

    # Get the product
    product = get_object_or_404(phonedetails, id=id)

    # Add to cart (or update quantity if already exists)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Quantity updated in cart")
    else:
        messages.success(request, "Item added to cart")

    return redirect('cart_view')




def cart_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first")
        return redirect('loginuser')

    user_id = request.user.id

    # Handle deletion
    if request.method == "POST":
        delete_id = request.POST.get("delete_id")
        if delete_id:
            Cart.objects.filter(
                id=delete_id,
                user=request.user   # 🔒 secure
            ).delete()
            return redirect('cart_view')

    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.phone_price * item.quantity

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )



def purchase(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart_view')

    total = sum(item.product.phone_price * item.quantity for item in cart_items)

    
    return redirect(cart_view)

