from django.contrib import admin
from .models import Commande, LignesCommande
from django.utils.safestring import mark_safe
import csv
import datetime
from django.utils.html import format_html
from django.http import HttpResponse
from django.urls import reverse

class CommandeLignesInline(admin.TabularInline):
  model = LignesCommande

  raw_id_fields = ['produit']
def commande_paiement(obj):
  url = obj.get_stripe_url()
  if obj.id_stripe:
    html = f'<a href="{url}" target="_blank">{obj.id_stripe}</a>'
    return mark_safe(html)
  return ''
commande_paiement.short_description = 'paiement_Stripe '

def order_detail(obj):
  url = reverse('commande:admin_order_detail', args=[obj.id])
  return mark_safe(f'<a href="{url}">View</a>')


def export_to_csv(modeladmin, request, queryset):
  opts = modeladmin.model._meta
  content_disposition = (
  f'attachment; filename={opts.verbose_name}.csv')
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = content_disposition
  writer = csv.writer(response)
  fields = [
  field
  for field in opts.get_fields()
    if not field.many_to_many and not field.one_to_many
  ]
     # Write a first row with header information
  writer.writerow([field.verbose_name for field in fields])
  #  Write data rows
  for obj in queryset:
   data_row = []
   for field in fields:
    value = getattr(obj, field.name)
    if isinstance(value, datetime.datetime):
      value = value.strftime('%d/%m/%Y')
    data_row.append(value)
   writer.writerow(data_row)
  return response
export_to_csv.short_description = 'Export to CSV'    

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
    'id',
    'prenom',
    'nom',
    'email',
    'adresse',
    'code_postal',
    'ville',
    'paye',
    'id_stripe',
    commande_paiement,
    'date_creation',
    'date_modification',
    order_detail,
    'pdf_link'
    
    ]
    actions=[export_to_csv]
    list_filter = ['paye', 'date_creation', 'date_modification']
    inlines = [CommandeLignesInline]

    def pdf_link(self, obj):
        url = reverse('commande:admin_order_pdf', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Exporter PDF</a>', url)
    pdf_link.short_description = 'PDF'
    pdf_link.allow_tags = True

# Register your models here.
