from django.test import TestCase
from  .models import *

# Create your tests here.
filEtudiant = Filiere.objects.all().order_by('nom_Fi')