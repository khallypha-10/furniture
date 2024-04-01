from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about-us/', views.about, name="about"),
    path('blogs/', views.blogs, name="blogs"),
    path('shop/', views.products, name="shop"),
    path('shop/<slug>', views.product, name="product"),
    path('services/', views.services, name="services"),
    path('add-to-cart/<slug>', views.add_to_cart, name="add"),
    path('remove-from-cart/<slug>', views.remove_from_cart, name="delete"),
    path("add-quantity/<slug>", views.add_quantity ,name="add-quantity"),
    path("reduce-quantity/<slug>", views.reduce_quantity ,name="reduce-quantity"),
    path('contact-us/', views.contact, name="contact"),
    path('register/', views.register, name="register"),
    path('payment/', views.PaymentView.as_view(), name="payment"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('checkout', views.CheckOutView.as_view(), name="checkout"),
    path('orders/<str:username>/', views.orders, name="orders"),
    path('edit-profile/<str:username>/', views.edit_profile, name="edit-profile"),
    path('cart/<str:user>/', views.cart, name="cart"),
    path('thank-you', views.thank_you, name="thank-you"),
    ]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)