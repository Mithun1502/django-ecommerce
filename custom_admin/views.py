from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order, Seller
from .forms import ProductForm, EditProductForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not hasattr(user, "seller"):
                return render(
                    request,
                    "admin_login.html",
                    {"error": "This is not a seller account"},
                )

            login(request, user)

            return redirect("dashboard")

    return render(request, "admin_login.html")


def seller_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("admin_login")

        if not hasattr(request.user, "seller"):
            return redirect("admin_login")

        return view_func(request, *args, **kwargs)

    return wrapper


@login_required(login_url="admin_login")
def dashboard(request):

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    total_products = Product.objects.filter(seller=request.user.seller).count()

    return render(request, "dashboard.html", {"total_products": total_products})


@seller_required
def products(request):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    products = Product.objects.filter(seller=request.user.seller)

    return render(request, "products.html", {"products": products})


@seller_required
def add_product(request):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)

            product.seller = request.user.seller

            product.save()

            return redirect("products")

    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})


@seller_required
def edit_product(request, id):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    product = Product.objects.get(id=id, seller=request.user.seller)

    if request.method == "POST":

        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("products")

        print(form.errors)

    else:
        form = EditProductForm(instance=product)

    return render(request, "edit_product.html", {"form": form, "product": product})


@seller_required
def delete_product(request, id):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    product = Product.objects.get(id=id, seller=request.user.seller)

    product.delete()

    return redirect("products")


@seller_required
def orders(request):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    all_orders = Order.objects.filter(product__seller=request.user.seller).order_by(
        "-created_at"
    )

    return render(request, "orders.html", {"orders": all_orders})


def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@seller_required
def view_product_admin(request, id):

    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not hasattr(request.user, "seller"):
        return redirect("admin_login")

    product = Product.objects.get(id=id, seller=request.user.seller)

    return render(request, "view_product_admin.html", {"product": product})


@seller_required
def seller_register(request):

    if request.method == "POST":

        shop_name = request.POST.get("shop_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(
                request, "seller_register.html", {"error": "Username already exists"}
            )

        user = User.objects.create_user(username=username, password=password)

        Seller.objects.create(user=user, shop_name=shop_name)

        return redirect("admin_login")

    return render(request, "seller_register.html")


@seller_required
def update_order_status(request, order_id):

    if request.method == "POST":

        order = Order.objects.get(id=order_id)

        order.status = request.POST.get("status")

        order.save()

    return redirect("orders")
