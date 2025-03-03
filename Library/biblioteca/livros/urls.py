from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('borrow_unit/<int:pk>/', views.borrow_book, name='borrow_book'),  # Mantenha apenas esta rota
    path('return/<int:loan_id>/', views.return_book, name='return_book'),
    path('manage_tags/', views.manage_tags, name='manage_tags'),
    path('backup/', views.backup, name='backup'),
    path('tags/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),
    path('emprestimo/', views.emprestimo_view, name='emprestimo'),
    path('import_backup/', views.import_backup, name='import_backup'),
    path('backup_list/', views.backup_list, name='backup_list'),
    path('loans/', views.list_loans, name='list_loans'),
    path('api/assistant/response/', views.get_assistant_response, name='assistant_response'),
    # path('available_units/', views.available_units, name='available_units'),  # Nova rota (opcional)
]