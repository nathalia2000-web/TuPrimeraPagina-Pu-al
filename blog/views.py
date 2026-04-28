from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from .models import Post, Categoria, Autor
from .forms import PostForm, AutorForm, CategoriaForm


# ✅ MIXIN personalizado
class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# ✅ CBV 1 - Lista de posts
class ListaPostsView(ListView):
    model = Post
    template_name = 'blog/lista_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(estado='publicado').order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


# ✅ CBV 2 - Detalle de post
class DetallePostView(DetailView):
    model = Post
    template_name = 'blog/detalle_post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(estado='publicado')


def home(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')[:6]
    contexto = {
        'posts': posts,
        'total_posts': Post.objects.count(),
        'total_autores': Autor.objects.count(),
        'total_categorias': Categoria.objects.count(),
    }
    return render(request, 'blog/home.html', contexto)


def lista_posts(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')
    categorias = Categoria.objects.all()
    contexto = {
        'posts': posts,
        'categorias': categorias,
    }
    return render(request, 'blog/lista_posts.html', contexto)


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug, estado='publicado')
    contexto = {
        'post': post,
    }
    return render(request, 'blog/detalle_post.html', contexto)


def posts_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(categoria=categoria, estado='publicado')
    contexto = {
        'categoria': categoria,
        'posts': posts,
    }
    return render(request, 'blog/lista_posts.html', contexto)


@login_required
def crear_post(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:lista_posts')
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html', {'form': form})


@login_required
def editar_post(request, slug):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detalle_post', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_post.html', {'form': form, 'post': post})


@login_required
def eliminar_post(request, slug):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:lista_posts')
    return render(request, 'blog/eliminar_post.html', {'post': post})


@login_required
def crear_autor(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = AutorForm()
    return render(request, 'blog/crear_autor.html', {'form': form})


@login_required
def crear_categoria(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = CategoriaForm()
    return render(request, 'blog/crear_categoria.html', {'form': form})


def buscar_posts(request):
    titulo    = request.GET.get('titulo', '')
    autor     = request.GET.get('autor', '')
    categoria = request.GET.get('categoria', '')

    posts = Post.objects.filter(estado='publicado')

    if titulo:
        posts = posts.filter(titulo__icontains=titulo)
    if autor:
        posts = posts.filter(autor__nombre__icontains=autor)
    if categoria:
        posts = posts.filter(categoria__nombre__icontains=categoria)

    contexto = {
        'posts': posts,
        'query': titulo,
    }
    return render(request, 'blog/buscar_posts.html', contexto)

