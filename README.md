# 📝 Mi Blog - Django

Blog desarrollado con Django y Bootstrap 5 que permite crear, editar, eliminar y buscar posts.

---

## 🛠️ Tecnologías utilizadas

- Python 3
- Django
- Bootstrap 5
- SQLite

---

## ⚙️ Instalación y configuración

### 1. Clona el repositorio
```bash
git clone https://github.com/Nathalia2000-web/mi-blog.git
cd mi-blog
## 📋 Pasos de uso

### ✅ Paso 1 - Crear un Autor
- Ve al menú **"Nuevo Autor"**
- URL: `/autor/nuevo/`
- Llena el formulario y guarda

### ✅ Paso 2 - Crear una Categoría
- Ve al menú **"Nueva Categoría"**
- URL: `/categoria/nueva/`
- Llena el formulario y guarda

### ✅ Paso 3 - Crear un Post
- Ve al menú **"Nuevo Post"**
- URL: `/post/nuevo/`
- Selecciona el autor y categoría creados anteriormente
- Llena el formulario y guarda

### ✅ Paso 4 - Ver el Post
- En la página de inicio verás la tarjeta del post
- URL: `/`
- Haz clic en **"👁️ Ver post"**

### ✅ Paso 5 - Editar el Post
- Desde el detalle del post
- URL: `/post/<id>/editar/`
- Haz clic en **"✏️ Editar"**
- Modifica los campos y guarda

### ✅ Paso 6 - Eliminar el Post
- Desde el detalle del post
- URL: `/post/<id>/eliminar/`
- Haz clic en **"🗑️ Eliminar"**
- Confirma la eliminación

### ✅ Paso 7 - Buscar Posts
- Ve al menú **"Buscar"**
- URL: `/buscar/`
- Filtra por título, autor o categoría