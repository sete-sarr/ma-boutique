# Ma Boutique

## Présentation

`mon_boutique` est une application e-commerce Django modulaire qui couvre le catalogue produit, la gestion de panier, la création de commande, le paiement Stripe, et l’administration des commandes.

## Fonctionnalités principales

- Catalogue produit
  - pages d’accueil et liste produits
  - navigation par catégorie
  - fiche produit détaillée avec ajout au panier
- Gestion de panier
  - panier stocké en session utilisateur
  - ajout, suppression, mise à jour de quantité
  - calcul automatique du prix total
- Commandes
  - formulaire de commande client
  - enregistrement des lignes de commande
  - génération PDF de facture côté admin
- Paiement Stripe
  - Stripe Checkout pour le paiement sécurisé
  - webhook Stripe pour validation du paiement
  - suivi du statut `paye` dans la commande
- Envoi d’email asynchrone
  - tâche Celery pour envoi d’email de confirmation de commande
- Administration
  - exporter les commandes au format CSV
  - lien direct vers le paiement Stripe
  - vue de détail commande

## Architecture modulaire

L’application est structurée en quatre apps Django dédiées :

- `boutique` : catalogue, catégories, pages publiques
- `panier` : logique panier côté session utilisateur
- `commande` : modèle commande, lignes de commande, formulaire de saisie
- `paiements` : intégration Stripe, pages de paiement et webhook

Le projet global `ma_boutique` centralise les paramètres, les URLs principales et la configuration Celery.

## Technologies utilisées

- Python 3
- Django 6.0
- SQLite pour la base de données locale
- Stripe API (`stripe==14.1.0`) pour les paiements
- Celery + RabbitMQ (`amqp://guest:guest@localhost:5672//`) pour le traitement asynchrone
- Django templates + `static/` + `media/`
- `python-decouple` pour la configuration sécurisée des clés
- `reportlab` pour produire des PDF de commande

## Requêtes optimisées et bonnes pratiques

- `Produit.objects.filter(id__in=id_produits)` pour limiter les requêtes dans le panier
- `Paginator` pour paginer les listes de produits
- `order_by` pour maîtriser le tri et profiter des index
- Index déclarés sur les modèles :
  - `Produit` : `nom`, `date_creation`, `prix`
  - `Commande` : `date_creation`, `prenom`
- `get_object_or_404` pour sécuriser l’accès aux objets
- `session.modified = True` pour garantir la persistance du panier

## Sécurité

- middleware CSRF activé dans `settings.py`
- `@csrf_exempt` uniquement sur le webhook Stripe, avec vérification de signature
- variables sensibles externes :
  - `CLE_PUBLIQUE_STRIPE`
  - `CLE_SECRET_STRIPE`
  - `STRIPE_WEBHOOK_SECRET`
- `DEBUG = False` en production, `ALLOWED_HOSTS` configuré
- validation de mot de passe Django activée
- pas de stockage d’informations de carte de crédit côté serveur
- le panier reste en session et ne stocke que les références produit et quantités


### Gestion du panier

- `POST /panier/ajouter/<int:id_produit>/`
  - ajoute un produit au panier ou met à jour la quantité
  - payload : `quantite`, `modifier`
- `GET /panier/panier/`
  - affiche le contenu du panier
- `GET /panier/supprimer/<int:id_produit>/`
  - supprime un produit du panier

### Commande

- `POST /commande/commande/`
  - crée une commande à partir du panier
  - payload : `prenom`, `nom`, `email`, `adresse`, `code_postal`, `ville`
- `GET /commande/admin/order/<int:order_id>/`
  - vue de détail commande pour l’administration
- `GET /commande/admin/order/<int:order_id>/pdf/`
  - export PDF de la commande

### Paiement

- `GET /paiements/processus/`
  - affiche la page de démarrage du paiement
- `POST /paiements/processus/`
  - crée une session Stripe Checkout
- `GET /paiements/reussir/`
  - page de confirmation de paiement
- `GET /paiements/annuler`
  - page d’annulation
- `POST /paiements/webhook/`
  - webhook Stripe pour validation de paiement et mise à jour du statut commande

## Instructions d’installation

1. Cloner le dépôt
2. Créer un environnement virtuel Python
3. Installer les dépendances :
   `pip install -r requirements.txt`
4. Configurer les variables d’environnement :
   `CLE_PUBLIQUE_STRIPE`, `CLE_SECRET_STRIPE`, `STRIPE_WEBHOOK_SECRET`
5. Appliquer les migrations :
   `python manage.py migrate`
6. Lancer RabbitMQ ou un broker compatible AMQP
7. Démarrer un worker Celery :
   `celery -A mon_boutique worker --loglevel=info`
8. Lancer l’application Django :
   `python manage.py runserver`

## Points d’amélioration possible

- basculer de SQLite vers PostgreSQL en production
- activer `AUTH_USER` pour comptes clients
- ajouter des tests unitaires et d’intégration
- configurer un backend email SMTP réel
- ajouter des mesures de performance supplémentaires côté requêtes et cache

## Notes spécifiques

- `commande_cree` envoie un email de confirmation via Celery
- `stripe_webhook` vérifie la signature Stripe avant toute mise à jour
- `Panier` est un wrapper session centralisé utilisé dans les vues panier et commandes
- `paiements.processus_paiement` recalcule les lignes de commande avant de créer la session Stripe

