from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_now, name='homepage'),  # 👈 new default homepage
    path('generate/', views.generate_codes, name='generate_codes'),
    path('print/', views.print_page, name='print_page'),
    path('register/', views.register_participants, name='register_participants'),
    path('delete-all-codes/', views.delete_all_codes, name='delete_all_codes'),
]
