from django.urls import path
from . import views

urlpatterns = [
	path('upload', views.upload, name='upload'),
	path('',views.signIn),
    path('postsign/',views.postsign),
    path('logout/',views.logout,name="log"),
    path('signup/',views.signUp,name='signup'),
    path('postsignup/',views.postsignup,name='postsignup'),
    path('create/',views.create,name='create'),
    path('post_create/',views.post_create,name='post_create'),
    path('check/',views.check,name='check'),
    path('post_check/',views.post_check,name='post_check'),
    path('delete/',views.delete,name='delete'),
    path('change/',views.change,name='change'),
    path('post_change/',views.post_change,name='post_change'),
    path('start/',views.start,name='start'),
]