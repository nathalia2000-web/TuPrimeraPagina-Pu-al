from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('post/<slug:slug>/editar/', views.editar_post, name='editar_post'),
    path('post/<slug:slug>/eliminar/', views.eliminar_post, name='eliminar_post'),
    path('categoria/<slug:slug>/', views.posts_por_categoria, name='posts_por_categoria'),
    path('crear-post/', views.crear_post, name='crear_post'),
    path('crear-autor/', views.crear_autor, name='crear_autor'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
]
