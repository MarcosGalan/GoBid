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

from core.views import home

admin.site.site_header = 'GoBid'  # Personaliza el encabezado del panel de administración
admin.site.site_title = 'GoBid'  # Personaliza el título del panel de administración

urlpatterns = [
    path('', home, name="home"),
]
