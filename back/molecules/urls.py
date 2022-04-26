from django.urls import path
from . import views

urlpatterns = [
    path('smiles/<str:smiles>', views.smiles, name="smiles"),
]
