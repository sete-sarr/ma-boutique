from celery import shared_task
from django.core.mail import send_mail

from .models import Commande
@shared_task
def commande_cree(id_commande):
   commande = Commande.objects.get(id=id_commande)
   sujet = f'Commande numero {commande.id}'
   message = (
        f"Mr {commande.prenom} :\n"
        f"Votre commande a été faite avec succès.\n"
        f"Votre numéro de commande : {commande.id}"
    )
   email_envoye = send_mail(subject=sujet,
                             message=message,
                               from_email='admin@gmail.com',
                                 recipient_list=[commande.email] 
                                 )
   return email_envoye
    