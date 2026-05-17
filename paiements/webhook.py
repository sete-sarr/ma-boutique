import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from commande.models import Commande

stripe.api_key = settings.STRIPE_SECRET_CLE

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if (
            session['mode'] == 'payment'
            and session['payment_status'] == 'paid'
        ):
            commande_id = session.get('client_reference_id')

            if not commande_id:
                print("❌ client_reference_id manquant")
                return HttpResponse(status=200)

            try:
                commande = Commande.objects.get(id=commande_id)
            except Commande.DoesNotExist:
                print("❌ Commande introuvable :", commande_id)
                return HttpResponse(status=200)

            # ✅ Marquer comme payée
            commande.paye = True
            commande.id_stripe = session.get('payment_intent')
            commande.save()

            print("✅ Commande payée avec succès :", commande.id)

    return HttpResponse(status=200)
