# Generated by Django 4.2 on 2025-02-27 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0004_remove_book_available_remove_book_available_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, to='livros.tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Título'),
        ),
    ]
