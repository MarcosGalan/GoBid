"""
URL configuration for GoBid project.

The `urlpatterns` list routes URLs to templates. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function templates
    1. Add an import:  from my_app import templates
    2. Add a URL to urlpatterns:  path('', templates.home, name='home')
Class-based templates
    1. Add an import:  from other_app.templates import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from products.views import products, product, UserItems, ItemUpdateView, ItemCreateView,ProductListApiView

urlpatterns = [
    path('', products.as_view(), name="products"),
    path('product/<int:pk>', product.as_view(), name="product"),
    path('user/items', UserItems.as_view(), name="user-items"),
    path('user/item/<int:pk>/', ItemUpdateView.as_view(), name="user-item"),
    path('user/item/', ItemCreateView.as_view(), name="user-item-create"),
    path('fetch/', ProductListApiView.as_view(), name='api-products'),
]
