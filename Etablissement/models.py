from django.db import models

# Create your models here.


class Departement(models.Model ):
    Abrreviation_Dep = models.CharField(max_length=10, blank=False, null=False,default=None)
    nom_Dep = models.CharField(max_length=50 , blank=False, null=False)
    image_Dep = models.ImageField(default='img/img1.jpg', upload_to='img')

    
    def __str__(self):
        return self.Abrreviation_Dep

class Filiere(models.Model):
    Abrreviation_Fi = models.CharField(max_length=10,blank=False, null=False,default=None)
    nom_Fi = models.CharField(max_length=50 , blank=False, null=False)
    Departement = models.ForeignKey(Departement, on_delete=models.CASCADE, blank= False , null=False)
    image_Fi = models.ImageField(default='img/img1.jpg', upload_to='img')

    
    def __str__(self):
        return self.Abrreviation_Fi





    








