from django.urls import path

from .views import *



urlpatterns = [
    path('', index, name='index'),

    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    
    path('dog/<str:category>/', dog_list, name='dog_list_url'),
    path('dog/<str:category>/add_new_dog/', AddDog.as_view(), name='add_new_dog_url'),
    path('dog/<str:category>/<str:slug>/', dog_page, name='dog_page_url'),
    path('dog/<str:category>/<str:slug>/update_dog', UpdateDog.as_view(), name='update_dog_url'),
    path('dog/<str:category>/<str:slug>/delete_dog', DeleteDog.as_view(), name='delete_dog_url'),

    path('contact', contact, name='contact')
] 