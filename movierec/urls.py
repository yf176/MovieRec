"""movierec URL Configuration

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

from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from user import urls

urlpatterns = [
    path('admin', admin.site.urls),
    url('user/', include('user.urls')),
    url('movies/', include('movies.urls')),
    url('rec/', include('rec.urls')),
    url('rating/', include('rating.urls')),
    url('portrait/', include('portrait.urls')),
    url('monitor/', include('monitor.urls')),
]
