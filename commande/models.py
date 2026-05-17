from django.db import models
from boutique.models import Produit
from django.conf import settings
class Commande(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField()
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    paye = models.BooleanField(default=False)
    id_stripe = models.CharField(max_length=200, blank=True)
    class Meta:
        ordering = ['-date_creation']
        indexes = [
        models.Index(fields=['date_creation','prenom']),
        ]
    def __str__(self):
       return f'Commande numero {self.id}'
    def get_prix_total(self):
       return sum(element.get_prix() for element in self.lignes.all())
    def get_stripe_url(self):
      if not self.id_stripe:
      # no payment associated
        return ''
      if '_test_' in settings.STRIPE_SECRET_CLE:
         path = '/test/'
      else:
     # Stripe path for real payments
       path = '/'
      return f'https://dashboard.stripe.com{path}payments/{self.id_stripe}'   

     # Create your models here.
class LignesCommande(models.Model):
    commande = models.ForeignKey(
    Commande,
    related_name='lignes',
    on_delete=models.CASCADE
    )
    produit = models.ForeignKey(
     'boutique.Produit',
      related_name='elements_commande',
      on_delete=models.CASCADE
      )
    prix = models.DecimalField(
       max_digits=10,
      decimal_places=2
      )
    quantite = models.PositiveIntegerField(default=1)
    def __str__(self):
      return str(self.id)
    def get_prix(self):
      return self.prix * self.quantite
