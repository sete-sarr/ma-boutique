from django.urls import path
from .import views
app_name = 'panier'
urlpatterns=[
    path('panier/',
          views.detail_panier,
          name='detail_panier'),

    path('ajouter/<int:id_produit>/',
          views.ajouter_au_panier,
            name='ajouter_au_panier'),

    path('supprimer/<int:id_produit>/',
          views.supprimer_panier,
          name='supprimer_panier'),
]