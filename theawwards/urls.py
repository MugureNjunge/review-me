from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('',views.index, name='index'),

    path('profiles/',views.profile_list, name='profile_api'),
    path('projects/',views.project_list, name='project_api'),
    
    path('sign-up/',views.register,name='sign-up'),
    path('accounts/sign-in/',views.signin,name='sign-in'),
    path('sign-out/', views.signout, name='sign-out'),

    path('profile/', views.UserProfile, name='profile'),
    path('profile/edit', views.EditProfile, name='profile/edit'),
    path('newproject', views.NewProject, name='newproject'),

    path('search/', views.search, name='search'),
    path('rating/',views.add_rating,name='rating'),
    
    path('profiles/<int:id>', views.profile_detail),
    path('projects/<int:id>', views.project_detail),

    
    
    
    


]

urlpatterns=format_suffix_patterns(urlpatterns)