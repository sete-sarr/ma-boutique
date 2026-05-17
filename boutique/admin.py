from django.contrib import admin
from .models import Categorie, Produit
@admin.register(Categorie)
class AdminCategorie(admin.ModelAdmin):
    list_display=['nom', 'slug']
    list_filter=['nom']
    prepopulated_fields={'slug':['nom']}
@admin.register(Produit)
class AdminProduit(admin.ModelAdmin):
    list_display=['categorie',
                 'nom', 'quantite',
                 'prix', 'disponibilite',
                 'date_creation', 'date_modification',
                 'statue',
                 'image','description']
    raw_id_fields=['categorie']
    list_filter=['categorie', 'nom',
                 'prix','disponibilite',
                 'date_creation','statue']
    

# Register your models here.
