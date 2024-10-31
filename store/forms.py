from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import Product


# Formulário para registro de usuários
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# Formulário para cadastro de salas
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "space_type",
            "features",
            "image",
            "on_sale",
            "available_from",
            "available_to",
        ]
        labels = {
            "name": "Nome da Sala",
            "price": "Preço",
            "space_type": "Tipo de Espaço",
            "features": "Características",
            "image": "Imagem",
            "on_sale": "Em Promoção",
            "available_from": "Disponível a partir de",
            "available_to": "Disponível até",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none'
            }),
            "price": forms.NumberInput(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none'
            }),
            "space_type": forms.Select(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none'
            }),
            "features": forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none'
            }),
            "image": forms.ClearableFileInput(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none'
            }),
            "on_sale": forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-sky-950 cursor-pointer focus:outline-none'
            }),
            "available_from": forms.DateInput(attrs={
                'type': 'date',
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none',
                'min': now().date()  # Define a data mínima para hoje
            }),
            "available_to": forms.DateInput(attrs={
                'type': 'date',
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none',
                'min': now().date()  # Define a data mínima para hoje
            })
        }