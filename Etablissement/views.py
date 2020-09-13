
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from  django.db import transaction
from django.contrib.auth.decorators import login_required
from  .decorators import *
from . import  query
from django.contrib.auth.models import Group

from .whatsappTwilio import sendMessage

from . import models
from  userProfiles.models import *
from .forms import *

@unauthenticated_user
def registerPage(request):

        #form2 = ProfileForm()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
            #form2 = ProfileForm(request.POST)

        if form.is_valid() :
            user=form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name__iexact="ETUDIANTS")
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            messages.error(request, form.error_messages)
    context = {'form': form} #'form2':form2
    return render(request, 'etablissement/signup.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        nom = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=nom, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'etablissement/index.html', context)
@login_required(login_url='login')
def welcome(request):
    context ={}
    return render(request,'etablissement/welcome.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['ENSEIGNANTS','admin'])
def home(request):
    from . import models
    #get phonenumber of all students
    stud_number = []
    departements = models.Departement.objects.all()
    for us in query.get_stud:
        phone = Profile.objects.get(user = us.id).phone_number
        stud_number.append(phone)

    #send the message
    if request.method == 'POST':
        messa  = request.POST.get('message')
        u = request.user.username
        mess = f'{messa}          \n\n\n\t\t\t\t signe:\t{u}'

        #img = models.Departement.objects.get(id=1).image_Dep.url
        #envoi du message
        for std in stud_number:
            sendMessage(std, mess)
            #sendMedia(std,mess,img)

    departements = models.Departement.objects.all()
    context={'departements':departements}
    return render(request, 'etablissement/departement.html',context)

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('myProfile')
        else:
            messages.error(request, 
            ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)


    user = request.user._get_pk_val()
    profile = Profile.objects.get(id=user)
  
    context = {'profile' : profile,
    'user_form': user_form,
    'profile_Form': profile_form
    }
    return render(request, 'etablissement/profile.html', context)



@login_required(login_url='login')
def profile(request):
    context = {}
    return render(request , 'etablissement/profile.html', context)


@login_required(login_url='login')
def sendDepartement(request,id_dep):

    phones = query.phone_Dep("ETUDIANTS",id_dep)
    from . import models
    filieres =models.Filiere.objects.filter(Departement_id=id_dep)
    # send the message
    if request.method == "POST":
        messa = request.POST.get('message')
        u = request.user.username
        mess = f'{messa}          \n\n\n\t\t\t\t signe:\t{u}'

        for ph in phones:
            sendMessage(ph,mess)

    context= {"filieres": filieres}
    return render (request, 'etablissement/filiere.html',context)

@login_required(login_url='login')
def sendFiliere(request,id_fi):
    phones = query.phone_Fi("ETUDIANTS", id_fi)


    # send the message
    if request.method == "POST":
        messa = request.POST.get('message')
        u = request.user.username
        mess = f'{messa}          \n\n\n\t\t\t\t signe:\t{u}'

        for ph in phones:
            sendMessage(ph, mess)
    context={}

    return render (request, 'etablissement/board.html',context)




def load_filieres(request):
    departement_id = request.GET.get('Departement_id')
    filieres = Filiere.objects.filter(Departement_id=departement_id)

    return render(request,'etablissement/ajax_load_filiere.html', {'filieres': filieres})




  
    


