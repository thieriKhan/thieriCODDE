from django.forms import ModelForm

from django.contrib.auth.models import User
from django import forms
from Etablissement.models import *
from userProfiles.models import Profile

from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):


    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    #email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        # widgets = {
        #     'username' :forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.TextInput(attrs={'class':'form-control'}),
        #     'password1' : forms.PasswordInput(attrs={'class':'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        # }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class ProfileForm(forms.ModelForm):
    # departement = forms.ModelChoiceField(queryset=Departement.objects.all(), empty_label=None)
    # filiere = forms.ModelChoiceField(queryset=Filiere.objects.get(Departement='departement'), empty_label=None)
    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'birth_date',
             'departement',
            'filiere',
            'specialite',
            'profile_image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filiere'].queryset = Filiere.objects.none()

        if 'departement' in self.data:
            try:
                departement_id = int(self.data.get('departement'))
                self.fields['filiere'].queryset = Filiere.objects.filter(Departement_id=departement_id).order_by('nom_Fi')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.departement is not  None :
                self.fields['filiere'].queryset = self.instance.departement.filiere_set.order_by('Abrreviation_Fi')
            





