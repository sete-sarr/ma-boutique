from django.urls import path
from . import views
app_name = 'commande'
urlpatterns=[
    path('commande/',
        views.view_creer_commande,
        name='creer_commande'),
        path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'),
        path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    ]