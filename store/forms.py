from datetime import timedelta

from django import forms
from django.forms.widgets import DateInput
from django.utils import timezone

from .models import Product


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
            "name": "Nome",
            "price": "Preço",
            "space_type": "Tipo de Espaço",
            "features": "Características",
            "image": "Imagem",
            "on_sale": "Em Promoção",
            "available_from": "Disponível a Partir de",
            "available_to": "Disponível Até",
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Define a data padrão para available_from e available_to
        # if "available_from" not in self.data and not self.instance.pk:
        #     self.fields["available_from"].initial = timezone.now().date()  # Data atual
        #     self.fields["available_to"].initial = timezone.now().date() + timedelta(
        #         days=3650
        #     )  # 10 anos à frente

        # Configurar widgets para formatar datas
        self.fields["available_from"].widget = DateInput(
            format="%d/%m/%Y",
            attrs={
                "type": "date",
                "min": str(timezone.now().date()),
                "max": str((timezone.now() + timedelta(days=365)).date()),
            },
        )
        self.fields["available_to"].widget = DateInput(
            format="%d/%m/%Y",
            attrs={
                "type": "date",
                "min": str((timezone.now() + timedelta(days=1)).date()),
                "max": str((timezone.now() + timedelta(days=365)).date()),
            },
        )

    def clean_features(self):
        features = self.cleaned_data.get("features")
        if not features:
            return "Nenhuma"
        return features
