from django.shortcuts import render
from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from commande.models import Commande

stripe.api_key = settings.STRIPE_SECRET_CLE
stripe.api_version = settings.STRIPE_API_VERSION

def processus_paiement(request):
    id_commande = request.session['id_commande']
    commande = get_object_or_404(Commande, id= id_commande)
    if request.method =='POST':
        url_succes = request.build_absolute_uri(reverse('paiements:reussi'))
        url_annulation = request.build_absolute_uri(reverse('paiements:annule'))
        donnees_session ={
            'mode':'payment',
            'success_url':url_succes,
            'cancel_url':url_annulation,
            'client_reference_id':commande.id,
            'line_items' :[]
        }
        for element in commande.lignes.all():
            donnees_session['line_items'].append(
               {
                  'price_data':{
                     'unit_amount':int(element.prix*Decimal('100') ),
                     'currency':'usd',
                     'product_data':{
                        'name' :element.produit.nom
                     },

                  },
                  'quantity': element.quantite
               }
            )
        session = stripe.checkout.Session.create(**donnees_session)
        return redirect(session.url, code=303)
    else:
     return render(request, 'paiements/paiement/processus.html', locals())
def paiement_accompli(request) :
   return render(request,  'paiements/paiement/reussi.html')   
def paiement_annule(request) :
   return render(request,  'paiements/paiement/annule.html') 

  




# Create your views here.
