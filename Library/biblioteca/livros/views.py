import os
import shutil
import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Book, Tag, Loan
from .forms import BookForm, LoanForm, ReturnForm, TagForm, BookUnit
from .forms import BorrowForm 
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)


# Função para verificar se o usuário é administrador
def is_admin(user):
    return user.is_staff



def index(request):
    query = request.GET.get('search', '')
    tag_filter = request.GET.get('tag', '')

    # Filtra unidades disponíveis com base no título do livro ou na tag
    units = BookUnit.objects.filter(available=True)
    if query:
        units = units.filter(book__title__icontains=query)
    if tag_filter:
        units = units.filter(book__tags__name=tag_filter)

    # Agrupa as unidades por livro e conta as disponíveis
    book_counts = {}
    for unit in units:
        book = unit.book
        if book not in book_counts:
            book_counts[book] = {
                'title': book.title,
                'unit_count': 0,
                'tags': book.tags.all(),
                'available': True  
            }
        book_counts[book]['unit_count'] += 1

    # Paginação
    book_list = list(book_counts.values())
    paginator = Paginator(book_list, 10)  # 10 livros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()
    return render(request, 'livros/index.html', {
        'page_obj': page_obj,
        'tags': tags,
        'query': query,
        'tag_filter': tag_filter
    })


    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'livros/login.html')

def user_logout(request):
    auth_logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('index')

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    books = Book.objects.all()
    loans = Loan.objects.all()
    tags = Tag.objects.all()
    return render(request, 'livros/admin_panel.html', {'books': books, 'loans': loans, 'tags': tags})

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Isso agora deve salvar também as tags corretamente
            messages.success(request, 'Livro adicionado com sucesso!')
            return redirect('admin_panel')
        else:
            print("❌ Erros no formulário:", form.errors)  # Depuração
    else:
        form = BookForm()
    return render(request, 'livros/add_book.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('admin_panel')
    else:
        form = BookForm(instance=book)
    return render(request, 'livros/edit_book.html', {'form': form, 'book': book})

@login_required

def borrow_book(request, pk):
    unit = get_object_or_404(BookUnit, id=pk, available=True)  # Verifica se a unidade está disponível
    
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            # Cria um novo empréstimo
            Loan.objects.create(
                book_unit=unit,
                student_name=form.cleaned_data['student_name'],
                student_id=form.cleaned_data['student_id']
            )
            # Atualiza o status da unidade para indisponível
            unit.available = False
            unit.save()
            messages.success(request, "Empréstimo confirmado com sucesso!")
            return redirect('index')  
        else:
            messages.error(request, "Erro ao processar o formulário. Por favor, verifique os campos.")
    else:
        form = BorrowForm()  # Cria uma instância vazia do formulário
    
    return render(request, 'livros/borrow.html', {'form': form, 'unit': unit})
@login_required
@user_passes_test(is_admin)
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, returned_date__isnull=True)
    if request.method == 'POST':
        form = ReturnForm(request.POST, instance=loan)
        if form.is_valid():
            # Salva a data de devolução
            loan.returned_date = timezone.now().date()
            loan.save()
            # Atualiza o status da unidade
            loan.book_unit.available = True
            loan.book_unit.save()
            messages.success(request, f'Unidade "{loan.book_unit.code}" do livro "{loan.book_unit.book.title}" devolvida com sucesso!')
            return redirect('list_loans')
    else:
        form = ReturnForm(instance=loan)
    return render(request, 'livros/return_book.html', {'form': form, 'loan': loan})


@login_required
@user_passes_test(is_admin)
def list_loans(request):
    loans = Loan.objects.filter(returned_date__isnull=True).select_related('book_unit', 'book_unit__book')
    return render(request, 'livros/list_loans.html', {'loans': loans})

@login_required
@user_passes_test(is_admin)
def manage_tags(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag adicionada com sucesso!')
            return redirect('manage_tags')
    else:
        form = TagForm()
    tags = Tag.objects.all()
    return render(request, 'livros/manage_tags.html', {'form': form, 'tags': tags})



@login_required
@user_passes_test(is_admin)
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, f'Tag "{tag.name}" excluída com sucesso!')
        return redirect('manage_tags')
    return render(request, 'livros/delete_tag_confirm.html', {'tag': tag})

@login_required
def emprestimo_view(request):
    query = request.GET.get('q', '')
    units = BookUnit.objects.filter(available=True)  # Filtra unidades disponíveis
    
    if query:
        units = units.filter(book__title__icontains=query)
    
    return render(request, 'livros/emprestimo.html', {'units': units, 'query': query})


@login_required
def backup(request):
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    db_path = settings.DATABASES['default']['NAME']
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'library_backup_{timestamp}.db'
    backup_path = os.path.join(backup_dir, backup_filename)
    try:
        shutil.copy(db_path, backup_path)
        messages.success(request, 'Backup realizado com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao fazer backup: {str(e)}')
    return redirect('admin_panel')



@login_required
def backup_list(request):
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    return render(request, 'livros/admin_panel.html', {'backups': backups})



@login_required
def import_backup(request):
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')
    db_path = settings.DATABASES['default']['NAME']

    if request.method == 'POST':
        # Verifica se é uma confirmação de importação
        if 'confirm_import' in request.POST:
            selected_backup = request.POST.get('selected_backup')
            backup_file_path = os.path.join(backup_dir, selected_backup)

            try:
                # Cria um backup temporário antes de substituir
                timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                temp_backup_path = os.path.join(backup_dir, f'temp_backup_{timestamp}.db')
                shutil.copy(db_path, temp_backup_path)

                # Substitui o banco de dados atual pelo backup selecionado
                shutil.copy(backup_file_path, db_path)

                # Registra o log
                logger.info(f"Backup importado: {selected_backup}")
                messages.success(request, 'Backup importado com sucesso!')
            except Exception as e:
                logger.error(f"Erro ao importar backup: {str(e)}")
                messages.error(request, f'Erro ao importar backup: {str(e)}')

            return redirect('admin_panel')
        
        elif 'backup_file' in request.FILES:
            backup_file = request.FILES['backup_file']
            try:
                # Salva o arquivo temporariamente
                with open(db_path, 'wb+') as destination:
                    for chunk in backup_file.chunks():
                        destination.write(chunk)

                # Registra o log
                logger.info(f"Backup importado via upload: {backup_file.name}")
                messages.success(request, 'Backup importado com sucesso!')
            except Exception as e:
                logger.error(f"Erro ao importar backup via upload: {str(e)}")
                messages.error(request, f'Erro ao importar backup: {str(e)}')

            return redirect('admin_panel')

    return redirect('admin_panel')

# Adicione esta função ao arquivo views.py

from django.http import JsonResponse

def get_assistant_response(request):
   
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        question = data.get('question', '').lower().strip()
        
        # Base de conhecimento
        knowledge_base = {
            "como faço para emprestar um livro": "Para emprestar um livro, navegue até a página do livro desejado, clique no botão 'Emprestar' e confirme a operação. O prazo padrão é de 14 dias.",
            "como renovar um empréstimo": "Para renovar um empréstimo, acesse a seção 'Livros Emprestados' e clique no botão 'Renovar' ao lado do livro que deseja renovar. Só é possível renovar se não houver reservas para o livro.",
            "onde vejo meus livros emprestados": "Seus livros emprestados podem ser visualizados na seção 'Livros Emprestados', acessível no menu superior (para administradores).",
            "como faço login no sistema": "Para fazer login, clique no botão 'Login' no canto superior direito e insira seu nome de usuário e senha.",
            "como fazer logout": "Para sair do sistema, clique no link 'Logout' no menu superior direito.",
            "como adicionar um livro": "Para adicionar um novo livro, você precisa ser administrador. Clique em 'Adicionar Livro' no menu superior e preencha o formulário com os detalhes do livro.",
            "como gerenciar tags": "Para gerenciar as tags (categorias) dos livros, você deve ser administrador. Acesse 'Gerenciar Tags' no menu superior para adicionar, editar ou remover tags.",
            "como fazer backup": "Para fazer backup do sistema, você deve ser administrador. Acesse 'Backup' no menu superior para iniciar o processo.",
            "para que serve o botão de vídeo": "O botão de vídeo com ícone de gato leva a um vídeo no YouTube que pode conter informações adicionais ou tutoriais sobre o sistema.",
            "o que posso fazer como administrador": "Como administrador, você pode adicionar livros, gerenciar tags, fazer backup do sistema, ver todos os livros emprestados e acessar o painel administrativo.",
            "como pesquisar livros": "Você pode pesquisar livros usando a barra de busca na página principal, filtrando por título, autor ou tags."
        }
        
        # Verificar correspondência exata
        if question in knowledge_base:
            return JsonResponse({"response": knowledge_base[question]})
        
        # Verificar palavras-chave
        for key in knowledge_base:
            # Dividir em palavras-chave para busca mais flexível
            key_words = key.split(' ')
            match_count = sum(1 for word in key_words if len(word) > 3 and word in question)
            
            # Se encontrou pelo menos 2 palavras-chave ou 50% das palavras
            if match_count >= 2 or match_count >= len(key_words) * 0.5:
                return JsonResponse({"response": knowledge_base[key]})
        
        # Resposta padrão se não encontrar correspondência
        return JsonResponse({
            "response": "Desculpe, não tenho informações sobre isso. Por favor, tente reformular sua pergunta ou entre em contato com a administração da biblioteca para assistência."
        })
    
    return JsonResponse({"error": "Método inválido. Use POST."})