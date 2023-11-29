from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.forms import ItemForm
from products.models import Product, Item, Category
from products.serializers import ProductSerializer, CategorySerializer


# Create your templates here.

class products(ListView):
    model = Product
    template_name = 'products/products.html'


class product(DetailView):
    model = Product
    template_name = 'products/product.html'


class UserItems(LoginRequiredMixin, View):
    template_name = 'products/user_items.html'
    login_url = 'access'

    def get(self, request, *args, **kwargs):
        items = Item.objects.filter(owner=request.user)

        return render(request, self.template_name, {'items': items})


class ItemUpdateView(LoginRequiredMixin, View):
    template_name = 'products/user_item.html'  # Ajusta esto según tu estructura de archivos de plantillas
    login_url = 'access'

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(instance=item, user=request.user)
        return render(request, self.template_name, {'form': form, 'item': item})

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(request.POST, instance=item, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-items')
        return render(request, self.template_name, {'form': form, 'item': item})


class ItemCreateView(LoginRequiredMixin, View):
    template_name = 'products/user_item.html'  # Ajusta esto según tu estructura de archivos de plantillas
    login_url = 'access'

    def get(self, request):
        form = ItemForm(user=request.user, )
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ItemForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-items')
        return render(request, self.template_name, {'form': form})


class ProductListApiView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        categories = Category.objects.all()

        product_serializer = ProductSerializer(products, many=True)
        category_serializer = CategorySerializer(categories, many=True)

        data = {
            'products': product_serializer.data,
            'categories': category_serializer.data,
        }

        return Response(data)

