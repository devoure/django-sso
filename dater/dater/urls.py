"""dater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from simple_sso.sso_client.client import Client
from django.conf import settings
from django.contrib.auth.views import LoginView


test_client = Client(settings.SSO_SERVER,
                     settings.SSO_PUBLIC_KEY,
                     settings.SSO_PRIVATE_KEY)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("dater/", include(test_client.get_urls())),
    path("dater/service1/", include('showdate.urls')),

    path("login/", LoginView.as_view(template_name='admin/login.html'), name="login"),
    path("logout/", LoginView.as_view(template_name='admin/logout.html'), name="logout")
]

