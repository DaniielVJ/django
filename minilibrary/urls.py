from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', views.index, name="indexMinilibrary"),
    # url para recibir el request con los datos del formulario
    path('recomendar/<int:book_id>', views.recomendar_libro, name="recomendar_libro"),
    path('review/<int:book_id>', views.add_review, name="add_review"),
    path('hello-fbv/', views.hello_fbv, name="hello_fbv"),
    path('hello-cbv/', views.HelloCBV.as_view(), name="hello_cbv"),
    path('welcome/', views.WelcomeView.as_view(), name="welcome_page"),
    path('books/', views.BookListView.as_view(), name="list_books"),
    # El parametro para buscar el objeto para mostrar su detalle debe llamarse pk para buscarlo por id
    # o slug para buscarlo por slug y indicar que se recibe un string
    path('books/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('books/<int:pk>/review', views.ReviewCreateView.as_view(), name="add_review2"),
    path('books/review/<int:pk>/update', views.ReviewUpdateView.as_view(), name="update_review"),
    path('books/review/<int:pk>/delete', views.ReviewDeleteView.as_view(), name="delete_review"),
    path('middleware/time', views.time_test, name="view_duration"),
    path('counter/', views.visit_counter),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]
