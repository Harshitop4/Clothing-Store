"""
URL configuration for endsem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup,name='signup'),
    path('logout/', views.logout,name='logout'),
    path('products/', views.products,name='products'),
    path('products/<int:pk>/', views.item,name='item'),
    path('cart/', views.cart,name='cart'),
    path('cart/remove/<int:pk>', views.cart_remove,name='cart_remove'),
    path('add_to_cart/<int:pk>', views.add_to_cart,name='add_to_cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('profile/', views.profile,name='profile'),
    path('buy/<int:pk>', views.buy,name='buy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)