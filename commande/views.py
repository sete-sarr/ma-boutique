from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande, LignesCommande
from .forms import FormCreerCommande
from panier.panier import Panier
from .tasks import commande_cree
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def view_creer_commande(request):
    panier = Panier(request)

    if request.method == 'POST':
        form = FormCreerCommande(request.POST)

        if form.is_valid():
            commande = form.save()

            for element in panier:
                LignesCommande.objects.create(
                    commande=commande,
                    produit=element['produit'],
                    prix=element['prix'],
                    quantite=element['quantite']
                )

            commande_cree.delay(commande.id)
            panier.vider()
            # return render(request, 'commande/cree.html',{
            #     'commande':commande
            # })  # ✅ IMPORTANT
            request.session['id_commande']=commande.id
            return redirect('paiements:processus')
        else:
            print("FORMULAIRE NON VALIDE")
            print(form.errors)  # 🔍 DEBUG
    else:
        form = FormCreerCommande()

    return render(request, 'commande/creer.html', {
        'form': form,
        'panier': panier
    })


def admin_order_detail(request, order_id):
    commande = get_object_or_404(Commande, id=order_id)
    return render(request, 'commande/detail.html', {'commande': commande})




def admin_order_pdf(request, order_id):
    # Récupérer la commande
    commande = get_object_or_404(Commande, id=order_id)

    # Préparer la réponse HTTP pour un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="commande_{commande.id}.pdf"'

    # Créer le PDF
    p = canvas.Canvas(response, pagesize=A4)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, f"Commande n°{commande.id}")

    # Informations client
    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Client : {commande.prenom} {commande.nom}")
    p.drawString(50, 750, f"E-mail : {commande.email}")
    p.drawString(50, 730, f"Adresse : {commande.adresse}, {commande.code_postal} {commande.ville}")
    p.drawString(50, 710, f"Montant total : {commande.get_prix_total}")
    p.drawString(50, 690, f"Status : {'Payé' if commande.paye else 'Paiement en attente'}")

    # Lignes de commande
    y = 670
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Produits achetés :")
    p.setFont("Helvetica", 12)
    for item in commande.lignes.all():
        y -= 20
        p.drawString(60, y, f"{item.produit.nom} - {item.quantite} x {item.prix} = {item.get_prix}")

    # Terminer le PDF
    p.showPage()
    p.save()
    return response


