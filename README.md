# Mon Boutique

Application Django de boutique en ligne.

## Fonctionnalités ajoutées / améliorées

- Pagination des produits dans la vue `boutique.views.liste_produit`.
- Affichage de 8 produits par page.
- Pagination intégrée dans le template `boutique/templates/boutique/produit/liste_produits.html`.
- Sidebar de catégories sans soulignement sur les liens.
- Sélection visuelle de la catégorie active.
- Correction du chargement de Bootstrap JavaScript dans `boutique/templates/base.html`.
- Gestion propre des cas où une catégorie ne contient aucun produit.

## Installation

1. Créez et activez un environnement virtuel :
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Installez les dépendances :
   ```powershell
   pip install -r requirements.txt
   ```
3. Appliquez les migrations :
   ```powershell
   python manage.py migrate
   ```
4. Lancez le serveur de développement :
   ```powershell
   python manage.py runserver
   ```

## Utilisation

- La page principale des produits est disponible à `/`.
- Les produits par catégorie s'affichent via `/categorie/<slug_categorie>`.
- Changez de page avec la pagination en bas de la liste de produits.

## Notes

- Le template principal utilise Bootstrap 5.
- Les liens de la sidebar sont stylés pour ne plus être soulignés.
