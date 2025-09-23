from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.signup, name='register'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='signout'),
    path('contact/', views.contact, name='contact'),
    path('documents/', views.documents, name='documents'),

    path('start_learning/', views.start_learning, name='start_learning'),
    path('videos/unlock/<int:video_id>/', views.unlock_video, name='unlock_video'),
]

