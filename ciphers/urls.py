from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("caesar_cipher", views.caesar_cipher_view, name="caesar_cipher"),
    path("update_opposite_result/", views.update_opposite_result, name="update_opposite_result"), 

    path('vigenere/', views.vigenere_cipher, name='vigenere'), 

    path('playfair_cipher/', views.playfair_cipher, name='playfair_cipher'),

    path('columnar-cipher/', views.columnar_cipher, name='columnar_cipher'),

    path('double-columnar/', views.double_columnar_cipher, name="double_columnar_cipher"),

    path('myteam/', views.myTeam, name='myteam'),
]
