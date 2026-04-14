from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('autor/nuevo/', views.crear_autor, name='crear_autor'),
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('post/nuevo/', views.crear_post, name='crear_post'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
    path('post/<int:pk>/', views.detalle_post, name='detalle_post'),
    path('post/<int:pk>/editar/', views.editar_post, name='editar_post'),
    path('post/<int:pk>/eliminar/', views.eliminar_post, name='eliminar_post'),
]