from django.conf import settings
from boutique.models import Produit
from decimal import Decimal
# class Panier:
#    def __init__(self, request):
#       self.session = request.session
#       panier = self.session.get[settings.ID_SESSION_PANIER]
#       if not panier:
#          self.panier.session[settings.settings.ID_SESSION_PANIER]={}
#       self.panier = panier 
#    def ajouter(self, quantite, modifier=False) :
#       id_produit = str(produit.id)
#       if id_produit not in self.panier:
#          self.panier[id_produit]={
#             'prix':str(produit.prix),
#              'quantite':0
#          }
#       if modifier :
#          self.panier[id_produit]['quantite']=quantite
#       else:
#          self.panier[id_produit]['quantite']+=quantite
#       self.enregistrer()    
#    def enregistrer(self):
#       self.session.modified= True 
#    def supprimer(self, produit) :
#       id_produit = str(produit.id)
#       if id_produit in self.panier:
#          del self.panier[id_produit]
#          self.enregistrer


# class Panier:
#     def __init__(self, request):
#         self.session = request.session
#         panier = self.session.get(settings.ID_SESSION_PANIER) 
#         if not panier:
#             self.session[settings.ID_SESSION_PANIER]={}
#         self.panier = panier
#     def ajouter(self, produit, quantite, modifier =False):
#         id_produit = str(produit.id)
#         if id_produit not in self.panier :
#             self.panier[id_produit]={
#                 'prix':str(produit.prix),
#                 'quantite':0
#             } 
#         if id_produit in self.panier :
#             self.panier[id_produit]['quantite'] = quantite
#         else: 
#             self.panier[id_produit]['quantite'] += quantite
#         self.enregistrer()
#         def enregistrer (self):
#             self.session.modified = True 
#     def supprimer(self, produit) :
#         id_produit = str(produit.id)
#         if id_produit in self.panier:
#           del self.panier[id_produit]
#           self.enregistrer()
#     def __iter__(self):
#         id_produits = self.panier.keys()
#         produits = Produit.objects.filter(id__in=id_produits)
#         panier = self.panier.copy() 
#         for produit in produits:
#          panier=[str(produit.id)]['produit']= produit
#         for element in self.panier.values() :
#             element['prix']=Decimal(element['prix'])
#             element['prix_total']= element['prix']*element['quantite']
#             yield element
#     def __len__(self):
#          return sum(element['quantite'] for element in self.panier.values())
#     def get_prix_total(self) :
#         return sum(Decimal(element['prix'])* element['quantite']  
#                    for element in self.panier.values())
#     def vider(self):
#         del self.session[settings.ID_SESSION_PANIER]
#         self.enregistrer()     
           
                   

                      
from decimal import Decimal
from django.conf import settings
from boutique.models import Produit

class Panier:
    def __init__(self, request):
        self.session = request.session
        panier = self.session.get(settings.ID_SESSION_PANIER)

        if panier is None:
            panier = self.session[settings.ID_SESSION_PANIER] = {}

        self.panier = panier

    def ajouter(self, produit, quantite=1, modifier=False):
        id_produit = str(produit.id)

        if id_produit not in self.panier:
            self.panier[id_produit] = {
                'prix': str(produit.prix),
                'quantite': 0
            }

        if modifier:
            self.panier[id_produit]['quantite'] = quantite
        else:
            self.panier[id_produit]['quantite'] += quantite

        self.enregistrer()

    def enregistrer(self):
        self.session.modified = True

    def supprimer(self, produit):
        id_produit = str(produit.id)
        if id_produit in self.panier:
            del self.panier[id_produit]
            self.enregistrer()

    def __iter__(self):
        id_produits = self.panier.keys()
        produits = Produit.objects.filter(id__in=id_produits)
        panier = self.panier.copy()

        for produit in produits:
            panier[str(produit.id)]['produit'] = produit

        for element in panier.values():
            element['prix'] = Decimal(element['prix'])
            element['prix_total'] = element['prix'] * element['quantite']
            yield element

    def __len__(self):
        return sum(element['quantite'] for element in self.panier.values())

    def get_prix_total(self):
        return sum(
            Decimal(element['prix']) * element['quantite']
            for element in self.panier.values()
        )

    def vider(self):
        self.session.pop(settings.ID_SESSION_PANIER, None)
        self.enregistrer()
                        
         
         
   