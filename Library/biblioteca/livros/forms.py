from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now, make_aware, is_aware
from datetime import datetime, date
from .models import Book, Tag, BookUnit, Loan

class BookForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        label="Quantidade de Cópias",
        help_text="Informe quantas cópias deste livro deseja adicionar."
    )

    unit_codes = forms.CharField(
        required=False,
        help_text="Informe os códigos das unidades separados por vírgula."
    )
    
    tags = forms.CharField(
        required=False,
        help_text="Informe as tags separadas por vírgula."
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'tags']  # Adicione 'tags' aqui

    def clean_unit_codes(self):
        unit_codes_str = self.cleaned_data.get('unit_codes', '')
        unit_codes = [code.strip() for code in unit_codes_str.split(',') if code.strip()]

        quantity = self.cleaned_data.get('quantity')

        if quantity and len(unit_codes) != quantity:
            raise forms.ValidationError("O número de códigos deve corresponder à quantidade especificada.")

        if len(unit_codes) != len(set(unit_codes)):
            raise forms.ValidationError("Os códigos das unidades devem ser únicos.")

        return unit_codes_str

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        if commit:
            instance.save()

        unit_codes_str = self.cleaned_data.get('unit_codes', '')
        unit_codes = [code.strip() for code in unit_codes_str.split(',') if code.strip()]

        # Criar novas unidades do livro
        for code in unit_codes:
            BookUnit.objects.get_or_create(book=instance, code=code, defaults={'available': True})

        # Salvar as tags se necessário
        tags_str = self.cleaned_data.get('tags', '')
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        for tag in tags:
            tag_instance, created = Tag.objects.get_or_create(name=tag)
            instance.tags.add(tag_instance)  # Se 'tags' for um ManyToManyField no modelo

        return instance

class BorrowForm(forms.Form):
    student_name = forms.CharField(
        label="Nome do Aluno",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    student_id = forms.CharField(
        label="Número do Aluno",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ReturnForm(forms.ModelForm):
    return_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data de Devolução"
    )

    class Meta:
        model = Loan
        fields = ['return_date']

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        borrowed_date = self.instance.borrowed_date

        if isinstance(borrowed_date, date):
            borrowed_date = datetime.combine(borrowed_date, datetime.min.time())

        if not is_aware(borrowed_date):
            borrowed_date = make_aware(borrowed_date)

        if return_date and return_date <= borrowed_date:
            raise forms.ValidationError("A data de devolução deve ser posterior à data de empréstimo.")
        return return_date

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class LoanForm(forms.ModelForm):
    book_unit = forms.ModelChoiceField(
        queryset=BookUnit.objects.none(),
        label="Código do Livro",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Loan
        fields = ['book_unit', 'student_name', 'student_id']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Aluno'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do Aluno'}),
        }

    def __init__(self, *args, **kwargs):
        book = kwargs.pop('book', None)
        super(LoanForm, self).__init__(*args, **kwargs)
        if book:
            self.fields['book_unit'].queryset = BookUnit.objects.filter(book=book, available=True)

    def save(self, commit=True):
        loan = super().save(commit=False)
        loan.book_unit.available = False
        loan.book_unit.save()
        if commit:
            loan.save()
        return loan
