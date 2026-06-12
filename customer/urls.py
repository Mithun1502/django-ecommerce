from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("viewproduct/", views.viewproduct, name="viewproduct"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("delete/<int:product_id>/", views.deleteproduct, name="deleteproduct"),
    path(
        "increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity",
    ),
    path(
        "decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity",
    ),
    path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "customer_orders/",
        views.customer_orders,
        name="customer_orders",
    ),
]
