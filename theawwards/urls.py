from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),

]    