from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from custom_admin.models import Product
from .forms import RegisterForm, LoginForm, CheckoutForm
from custom_admin.models import Product, Order
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from custom_admin.models import Order
from .forms import EditProfileForm


def home(request):
    return render(request, "home.html")


def viewproduct(request):
    products = Product.objects.all()
    cart = request.session.get("cart", {})

    for product in products:
        product.in_cart = str(product.id) in cart
        product.cart_quantity = cart.get(str(product.id), 1)

    context = {
        "products": products,
    }

    return render(request, "viewproduct.html", context)


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            UserProfile.objects.create(user=user, mobile=form.cleaned_data["mobile"])

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:

                if hasattr(user, "seller"):
                    form.add_error(None, "Please login through seller portal")
                    return render(request, "login.html", {"form": form})

                auth_login(request, user)

                return redirect("home")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("login")


def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return JsonResponse({"success": True, "quantity": cart[product_id]})


def cart(request):

    cart = request.session.get("cart", {})

    cart_items = []
    grand_total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        total = product.price * quantity

        grand_total += total

        cart_items.append({"product": product, "quantity": quantity, "total": total})

    return render(
        request, "cart.html", {"cart_items": cart_items, "grand_total": grand_total}
    )


@login_required(login_url="login")
def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            address = form.cleaned_data["address"]

            profile = UserProfile.objects.get(user=request.user)
            profile.address = address
            profile.save()

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)

                total = product.price * quantity

                Order.objects.create(
                    customer_name=request.user.username,
                    customer_email=request.user.email,
                    product=product,
                    quantity=quantity,
                    total_price=total,
                    address=address,
                )
            request.session["cart"] = {}

            messages.success(request, "Order placed successfully!")

            return redirect("customer_orders")

    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form})


def deleteproduct(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def increase_quantity(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
        request.session["cart"] = cart

        return JsonResponse({"success": True, "quantity": cart[product_id]})

    return JsonResponse({"success": False})


def decrease_quantity(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

            request.session["cart"] = cart

            return JsonResponse(
                {"success": True, "quantity": cart[product_id], "removed": False}
            )

        else:

            del cart[product_id]

            request.session["cart"] = cart

            return JsonResponse({"success": True, "removed": True})

    return JsonResponse({"success": False})


def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("viewproduct")


from custom_admin.models import Order


@login_required(login_url="login")
def customer_orders(request):

    orders = Order.objects.filter(customer_email=request.user.email).order_by(
        "-created_at"
    )

    return render(
        request,
        "customer_orders.html",
        {"orders": orders},
    )


@login_required(login_url="login")
def profile(request):
    profile = UserProfile.objects.get(user=request.user)

    return render(request, "profile.html", {"profile": profile})



@login_required(login_url="login")
def customer_editprofile(request):

    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":

        form = EditProfileForm(request.POST, user=request.user)

        if form.is_valid():

            request.user.username = form.cleaned_data["username"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()

            profile.mobile = form.cleaned_data["mobile"]
            profile.address = form.cleaned_data["address"]
            profile.save()

            messages.success(request, "Profile updated successfully")

            return redirect("profile")

    else:

        form = EditProfileForm(
            user=request.user,
            initial={
                "username": request.user.username,
                "email": request.user.email,
                "mobile": profile.mobile,
                "address": profile.address,
            },
        )

    return render(request, "customer_editprofile.html", {"form": form})
