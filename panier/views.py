from django.shortcuts import redirect, render, get_object_or_404
from .panier import Panier
from boutique.models import Produit
from django.views.decorators.http import require_POST
from .forms import FormAdd

@require_POST
def ajouter_au_panier(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    formAjout = FormAdd(request.POST)
    if formAjout.is_valid():
        cd = formAjout.cleaned_data
        panier.ajouter(produit,
                       cd['quantite'],
                         cd['modifier'] 
                         )
    return redirect('panier:detail_panier') 
def supprimer_panier(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    panier.supprimer(produit)
    return redirect('panier:detail_panier')
def detail_panier(request):
    panier = Panier(request)
    for item in panier:
      item['actualiser_quantite_form'] = FormAdd(
      initial={'quantite': item['quantite'], 'modifier': True}
      )
    return render(request,
                   'panier/panier.html',
                   {'panier':panier})




# Create your views here..
