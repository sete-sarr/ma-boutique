from django import forms
choix_quantite_produit = [(i,str(i)) for i in range(1, 20)]
class FormAdd(forms.Form):
    quantite = forms.TypedChoiceField(
        choices=choix_quantite_produit,
        coerce=int)
    modifier = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput

    )
