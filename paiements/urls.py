from django.urls import include, path
from . import views
from .webhook import stripe_webhook
app_name = 'paiements'
urlpatterns=[
    path('processus/', views.processus_paiement, name='processus'),
    path('reussir/', views.paiement_accompli, name='reussi'),
    path('annuler', views.paiement_annule, name='annule'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]