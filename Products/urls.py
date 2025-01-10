from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name='get products'),
    path('products/add/', views.add_product, name='products'),
    path('products/update/<int:pk>/', views.updateProduct, name='update product'),
    path('products/delete/<int:pk>/', views.deleteProduct, name='delete product'),
    path('cart/add/', views.add_to_cart, name='add to cart'),
    path('cart/', views.get_cart_items, name='get cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item, name='update cart item'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='delete cart item'),
    path('checkout/', views.checkout, name='checkout'),
]
