from django.urls import path
from . import views

# lista con el patron de urls
urlpatterns = [
    path('home/', views.home, name='home'),
    path('stack/<str:tool>', views.stack_detail, name='stack')
]
