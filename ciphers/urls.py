from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("caesar_cipher", views.caesar_cipher_view, name="caesar_cipher"),
    path("update_opposite_result/", views.update_opposite_result, name="update_opposite_result"), 

    path('vigenere/', views.vigenere_cipher, name='vigenere'), 
    path('myteam/', views.myTeam, name='myteam'),
]
