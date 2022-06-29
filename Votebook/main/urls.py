from django.urls import path, include
from main import views
from rest_framework import routers


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('parties/', views.party_list),
    path('parties/<int:pk>/', views.party_detail),
    path('register-candidate/', views.register_candidate),
    path('register/', views.register_voter),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('vote/', views.vote),
    path('', views.index),
    path('results/', views.results),
]
