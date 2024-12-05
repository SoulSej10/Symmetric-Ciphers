from django.urls import path
from . import views

urlpatterns = [
    path("", views.caesar_cipher_view, name="caesar_cipher"),
    path("update_opposite_result/", views.update_opposite_result, name="update_opposite_result"), 

    path('vigenere/', views.vigenere_cipher, name='vigenere'), 
    path('myteam/', views.myTeam, name='myteam'),
]
