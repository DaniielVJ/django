from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="indexMinilibrary"),
    # url para recibir el request con los datos del formulario
    path('recomendar/<int:book_id>', views.recomendar_libro, name="recomendar_libro"),
    path('review/<int:book_id>', views.add_review, name="add_review")
]
