"""hopch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from app import views, challenges, access
from hopch.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [

    # Admin
    url(r'^admin/', admin.site.urls),

    # Index
    url(r'^$', views.index, name='index'),

    # Teach
    url(r'^challenges$', challenges.views, name='challenges'),

    # Access
    url(r'^access$', access.views, name='access'),
]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
