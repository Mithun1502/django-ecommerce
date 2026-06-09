from django.shortcuts import render, redirect
from .models import Product, Order
from .forms import ProductForm


def admin_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "1234":
            request.session["admin_logged_in"] = True
            return redirect("dashboard")

    return render(request, "admin_login.html")


def dashboard(request):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    total_products = Product.objects.count()

    context = {"total_products": total_products}

    return render(request, "dashboard.html", context)


def products(request):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    products = Product.objects.all()

    return render(request, "products.html", {"products": products})


def add_product(request):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("products")

    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})


def edit_product(request, id):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    product = Product.objects.get(id=id)

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("products")

    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {"form": form, "product": product})


def delete_product(request, id):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    product = Product.objects.get(id=id)

    product.delete()

    return redirect("products")


def orders(request):

    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    all_orders = Order.objects.all().order_by("-created_at")

    return render(request, "orders.html", {"orders": all_orders})


def admin_logout(request):

    if "admin_logged_in" in request.session:
        del request.session["admin_logged_in"]

    return redirect("admin_login")
