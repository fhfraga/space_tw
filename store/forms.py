from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        #fields = ['name', 'price', 'space_type', 'features', 'image', 'link', 'on_sale']
        fields = ['name', 'price', 'space_type', 'features', 'image', 'on_sale', 'available_from', 'available_to']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        # Define a data padrão para available_from e available_to
        if 'available_from' not in self.data and not self.instance.pk:
            self.fields['available_from'].initial = timezone.now().date()  # Data atual
            self.fields['available_to'].initial = timezone.now().date() + timedelta(days=3650)  # 10 anos à frente

    def clean_features(self):
        features = self.cleaned_data.get('features')
        if not features:
            return "Nenhuma"
        return features
