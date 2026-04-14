from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Autor, Categoria
from .forms import AutorForm, CategoriaForm, PostForm

def home(request):
    posts = Post.objects.filter(estado='publicado')
    total_posts = Post.objects.count()
    total_autores = Autor.objects.count()
    total_categorias = Categoria.objects.count()
    
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'total_autores': total_autores,
        'total_categorias': total_categorias,
    }
    return render(request, 'blog/home.html', context)

def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AutorForm()
    return render(request, 'blog/crear_autor.html', {'form': form})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoriaForm()
    return render(request, 'blog/crear_categoria.html', {'form': form})

def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html', {'form': form})

def buscar_posts(request):
    posts = Post.objects.all()

    titulo = request.GET.get('titulo', '')
    autor = request.GET.get('autor', '')
    categoria = request.GET.get('categoria', '')

    if titulo:
        posts = posts.filter(titulo__icontains=titulo)
    if autor:
        posts = posts.filter(autor__nombre__icontains=autor)
    if categoria:
        posts = posts.filter(categoria__nombre__icontains=categoria)

    return render(request, 'blog/buscar_posts.html', {'posts': posts})

def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detalle_post.html', {'post': post})

def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalle_post', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_post.html', {'form': form, 'post': post})

def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/eliminar_post.html', {'post': post})