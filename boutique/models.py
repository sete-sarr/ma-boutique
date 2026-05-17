from django.db import models
from django.urls import reverse
class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    def __str__(self):
        return self.nom
    def get_absolute_url(self):
        return reverse('boutique:produit_par_categorie', args=[self.slug])
class Produit(models.Model):
    categorie = models.ForeignKey(Categorie,
                                   related_name='produits',
                                   on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10,
                                decimal_places=2,)
    disponibilite = models.BooleanField(default=False,blank=True)
    quantite = models.IntegerField() 
    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    statue = models.BooleanField(default=False)
    def __str__(self):
        return self.nom
    class Meta:
        ordering=['-date_creation']
        indexes = [models.Index(fields=['nom',
                                         'date_creation',
                                         'prix']      
                    )]
    def get_absolute_url(self):
        return reverse()    
        
        

# Create  your models here.
