from django.contrib import admin
from .models import Book, BookUnit, Loan, Tag

class BookUnitInline(admin.TabularInline):
    model = BookUnit
    extra = 1  # Permite adicionar unidades diretamente no admin do livro

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tag_list')  # Exibe título, autor e tags
    search_fields = ('title', 'author')  # Permite pesquisar por título e autor
    filter_horizontal = ('tags',)  # Interface melhorada para selecionar tags
    inlines = [BookUnitInline]  # Permite gerenciar unidades diretamente no admin do livro

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = 'Tags'

@admin.register(BookUnit)
class BookUnitAdmin(admin.ModelAdmin):
    list_display = ('book', 'code', 'available')  # Exibe livro, código e status
    list_filter = ('available',)  # Filtra por disponibilidade
    search_fields = ('code', 'book__title')  # Permite pesquisar por código ou título do livro

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book_unit', 'student_name', 'student_id', 'borrowed_date', 'returned_date')
    list_filter = ('returned_date',)  # Filtra por data de devolução
    search_fields = ('book_unit__book__title', 'student_name', 'student_id')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)