from django.contrib import admin
from .models import Book, Tag, Loan

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available', 'quantity', 'available_quantity')
    search_fields = ('title', 'author')
    list_filter = ('available',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'student_name', 'student_id', 'borrowed_date', 'returned_date')
    search_fields = ('book__title', 'student_name', 'student_id')
    list_filter = ('borrowed_date', 'returned_date')

admin.site.register(Book, BookAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Loan, LoanAdmin)
