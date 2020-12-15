
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
    hide= False
    clear2= True
    request.get_host()
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
            msg = 'Account was created for ' + username
            messages.success(request, msg , extra_tags="alert")
           
       
            return redirect('login')
        else:
            messages.error(request,form.errors)
            
        
    context = {'form': form , 'hide':hide, 'clear2' : clear2} 
    return render(request, 'etablissement/signup.html', context)

@unauthenticated_user
def loginPage(request):
    clear= True
    if request.method == 'POST':
        nom = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=nom, password=password)
        
       

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    hide = False
    context = {'hide': hide, 'clear':clear  }
    return render(request, 'etablissement/index.html', context)

@login_required(login_url='login')
def welcome(request):
     hide = True
     context ={'hide':hide}
     return render(request,'etablissement/welcome.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['ENSEIGNANTS','admin'])
def home(request):
    hide= True
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
    context={'departements':departements , 'hide': hide}
    return render(request, 'etablissement/departement.html',context)

@login_required
@transaction.atomic
def update_profile(request):
    hide= True
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
    'profile_Form': profile_form, 
    'hide' : hide
    }
    return render(request, 'etablissement/profile.html', context)



@login_required(login_url='login')
def profile(request):
    hide = True
    context = { 'hide' : hide}
    return render(request , 'etablissement/profile.html', context)


@login_required(login_url='login')
def sendDepartement(request,id_dep):
    hide = True
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

    context= {"filieres": filieres,  'hide' : hide}
    return render (request, 'etablissement/filiere.html',context)

@login_required(login_url='login')
def sendFiliere(request,id_fi):
    phones = query.phone_Fi("ETUDIANTS", id_fi)
    hide = True

    # send the message
    if request.method == "POST":
        messa = request.POST.get('message')
        u = request.user.username
        mess = f'{messa}          \n\n\n\t\t\t\t signe:\t{u}'

        for ph in phones:
            sendMessage(ph, mess)
    context= {'hide' : hide}

    return render (request, 'etablissement/board.html',context)




def load_filieres(request):
    departement_id = request.GET.get('Departement_id')
    filieres = Filiere.objects.filter(Departement_id=departement_id)

    return render(request,'etablissement/ajax_load_filiere.html', {'filieres': filieres})




  
    


