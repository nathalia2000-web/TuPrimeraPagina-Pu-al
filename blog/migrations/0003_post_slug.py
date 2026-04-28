from django.db import migrations, models
from django.utils.text import slugify


def generar_slugs(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        post.slug = slugify(post.titulo)
        post.save()


class Migration(migrations.Migration):

    dependencies = [
           ('blog', '0002_post_imagen_alter_post_contenido'),  # ✅ Correcto
    ]

    operations = [
        # Primero agrega el campo SIN unique
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default=''),
            preserve_default=False,
        ),
        # Luego genera los slugs para posts existentes
        migrations.RunPython(generar_slugs),
        # Por último aplica el unique
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
    