from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_login, name="admin_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("add-product/", views.add_product, name="add_product"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("edit-product/<int:id>/", views.edit_product, name="edit_product"),
    path("delete-product/<int:id>/", views.delete_product, name="delete_product"),
    path("orders/", views.orders, name="orders"),
    path("view-product/<int:id>/", views.view_product_admin, name="view_product_admin"),
    path("seller-register/", views.seller_register, name="seller_register"),
    path(
        "update-order-status/<int:order_id>/",
        views.update_order_status,
        name="update_order_status",
    ),
    path(
        "seller-order-notifications/",
        views.seller_order_notifications,
        name="seller_order_notifications",
    ),
]
