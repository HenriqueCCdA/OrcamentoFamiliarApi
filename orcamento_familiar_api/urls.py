"""orcamento_familiar_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings

from orcamento_familiar_api.budget.views import receita, receitas, despesas, despesa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/receitas', receitas, name='receitas'),
    path('api/v1/receitas/<int:id>', receita, name='receita'),
    path('api/v1/despesas', despesas, name='despesas'),
    path('api/v1/despesas/<int:id>', despesa, name='despesa')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
