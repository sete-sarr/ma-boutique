from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Produit, Categorie
from django.forms import modelform_factory, inlineformset_factory
from django.db.models.signals import post_save
from panier.forms import FormAdd


def paginate_products(request, produits):
    paginator = Paginator(produits, 4)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def accueil(request):
    categories = Categorie.objects.all()
    produits_recents = Produit.objects.order_by('-date_creation')[:6]
    return render(
        request,
        'boutique/accueil.html',
        {
            'categories': categories,
            'produits_recents': produits_recents,
        },
    )


def produits(request):
    produits = Produit.objects.all().order_by('nom')
    categories = Categorie.objects.all()
    produits = paginate_products(request, produits)
    return render(
        request,
        'boutique/produit/liste_produits.html',
        {
            'produits': produits,
            'categories': categories,
            'categorie': None,
        },
    )


def liste_produit(request, slug_categorie=None):
    produits = Produit.objects.all().order_by('nom')
    categories = Categorie.objects.all()
    categorie = None

    if slug_categorie:
        categorie = get_object_or_404(Categorie, slug=slug_categorie)
        produits = Produit.objects.filter(categorie=categorie).order_by('nom')

    produits = paginate_products(request, produits)
    return render(
        request,
        'boutique/produit/liste_produits.html',
        {
            'produits': produits,
            'categories': categories,
            'categorie': categorie,
        },
    )


def contact(request):
    categories = Categorie.objects.all()
    return render(
        request,
        'boutique/contact.html',
        {
            'categories': categories,
        },
    )


def detail_produit(request, id):
    formAjout = FormAdd()
    produit = get_object_or_404(Produit, id=id)
    return render(
        request,
        'boutique/produit/detail_produit.html',
        {'produit': produit, 'formAjout': formAjout},
    )


# Create your views here.
