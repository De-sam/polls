from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_now, name='homepage'),
    path('generate/', views.generate_codes, name='generate_codes'),
    path('print/', views.print_page, name='print_page'),
    path('register/', views.register_participants, name='register_participants'),
    path('delete-all-codes/', views.delete_all_codes, name='delete_all_codes'),
    path('vote/', views.cast_vote, name='cast_vote'),  # 
    path('results/', views.view_results, name='view_results'),
    path('public-vote/', views.public_vote, name='public_vote'),


]
