from django import forms
from .models import Commande


class FormCreerCommande(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [
            'prenom',
            'nom',
            'email',
            'adresse',
            'code_postal',
            'ville',
            
        ]

        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adresse de livraison'
            }),
            'code_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code postal'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
           
        }
