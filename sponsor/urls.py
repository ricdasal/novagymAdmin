from django.urls import path
from .views import *
from .apps import SponsorConfig

app_name = SponsorConfig.name


urlpatterns = [
     path('create/', createSponsor, name='createSponsor'),
     path('sponsor-list/', sponsorList, name='sponsor-overview'),
     path('sponsor-detail/<str:id>', sponsorDetail, name='sponsor-detail'),
     path('sponsor-create/', sponsorCreate, name='sponsor-create'),
     path('sponsor-update/<str:id>', sponsorUpdate, name='sponsor-update'),
     path('sponsor-delete/<str:id>', sponsorDelete, name='sponsor-delete'),
]