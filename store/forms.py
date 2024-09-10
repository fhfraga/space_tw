from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'space_type', 'features', 'image', 'link', 'on_sale']
    
    def clean_features(self):
        features = self.cleaned_data.get('features')
        if not features:
            return "Nenhuma"
        return features

