from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)  # Indica se o livro está disponível no geral
    quantity = models.PositiveIntegerField(default=1)  # Quantidade total de cópias
    available_quantity = models.PositiveIntegerField(default=1)  # Cópias disponíveis atualmente
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title



class Loan(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)  # Relacionamento com o livro
    student_name = models.CharField(max_length=100, verbose_name="Nome do Aluno")
    student_id = models.CharField(max_length=20, verbose_name="Número do Aluno")
    borrowed_date = models.DateField(auto_now_add=True, verbose_name="Data do Empréstimo")  # Automática
    returned_date = models.DateField(null=True, blank=True, verbose_name="Data da Devolução")

    def __str__(self):
        return f"{self.book.title} - {self.student_name}"