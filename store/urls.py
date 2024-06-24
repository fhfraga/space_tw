from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('about/', views.about, name='about'), 
    path('rooms/sala_1', views.sala_aracatiba, name='sala_aracatiba'), 
    path('rooms/sala_2', views.sala_centro, name='sala_centro'), 
    path('rooms/sala_3', views.sala_itapeba, name='sala_itapeba'), 
    path('rooms/auditorio_1', views.auditorio_inoa, name='auditorio_inoa'), 
    path('checkout/', views.finish, name='finalizar'),
    path('shared_space/', views.shared_space, name='shared_space'),
    path('office-spaces/', views.office_spaces, name='office_spaces'),
    path('auditorium-spaces/', views.auditorium_spaces, name='auditorium_spaces'),
    path('search/', views.search_results, name='search_results'),
    path('api/validar_transacao/', views.validar_transacao, name='validar_transacao'),
    path('finish/', views.finish, name='finish'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
]