"""cpanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new

from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.signIn),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^signup/',views.signUp,name='signup'),
    url(r'^postsignup/',views.postsignup,name='postsignup'),
    url(r'^create/',views.create,name='create'),
    url(r'^post_create/',views.post_create,name='post_create'),
    url(r'^check/',views.check,name='check'),
    url(r'^post_check/',views.post_check,name='post_check'),
    url(r'^delete/',views.delete,name='delete'),
    url(r'^change/',views.change,name='change'),
    url(r'^post_change/',views.post_change,name='post_change'),
    url(r'^start/',views.start,name='start'),
    url(r'^upd/',views.upload_doc,name='upload_doc'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
