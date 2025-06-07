from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),   # 👈 this line is CRUCIAL
    path('', include('voting.urls')),   # 👈 this line is CRUCIAL

]
