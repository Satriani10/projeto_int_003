from django.contrib import admin
from .models import Book, Tag, Borrow

#admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Borrow)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'quantity', 'available_quantity', 'available')
    list_filter = ('available',)
    search_fields = ('title', 'author')