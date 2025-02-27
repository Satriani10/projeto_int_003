from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=100, verbose_name="Autor")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    def __str__(self):
        return self.title


class BookUnit(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='units')
    code = models.CharField(max_length=50, unique=True)  # Código único para cada unidade
    available = models.BooleanField(default=True)  # Status de disponibilidade da unidade

    def __str__(self):
        return f"{self.book.title} - Código: {self.code}"


class Loan(models.Model):
    book_unit = models.ForeignKey('BookUnit', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    borrowed_date = models.DateTimeField(auto_now_add=True)  # Data e hora do empréstimo
    returned_date = models.DateTimeField(null=True, blank=True)  # Data e hora da devolução

    def __str__(self):
        return f"{self.book_unit.book.title} - {self.student_name}"