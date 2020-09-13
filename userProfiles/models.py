from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from  django.db import  models
from Etablissement.models import *


# Create your models here.

class Profile(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, blank=True,null=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=False, null=True )
    birth_date = models.DateField(null=True, blank=True)
    specialite = models.CharField(null=True, blank=True, max_length=50)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='img/profile', null=True, blank=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()