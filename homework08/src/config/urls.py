"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import RedirectView

urlpatterns = [
    # Handle the root url.
    path('', RedirectView.as_view(url='notes/'), name='index'),

    # Accounts app
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # Notes app
    path('notes/', include('notes.urls', namespace='notes')),

    # Admin
    path('admin/', admin.site.urls),

    path('api/', include('api.urls', namespace='api')),
]
