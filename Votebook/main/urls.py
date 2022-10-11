from django.urls import path, include
from main import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/subjects/', views.subject_list),
    path('api/subjects/<int:id_subject>/', views.subject_detail),
    path('register/', views.register_voter, name='register'),
    path('login/', views.login_voter, name='login'),
    path('logout/', views.logout_voter, name='logout'),
    path('create/', views.create_subject, name='create'),
    path('subject_detail/<int:id_subject>/', views.subject_detail, name='subject_detail'),
    path('campaigns/', views.subjects, name='campaigns'),
    path('/', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
]
