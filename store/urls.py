from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('new-launches/', views.new_launches, name='new_launches'),
    path('festive-combos/', views.festive_combos, name='festive_combos'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/action/', views.cart_action, name='cart_action'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('checkout/success/<str:order_id>/', views.order_success, name='order_success'),
    path('search/', views.search_products, name='search_products'),
]