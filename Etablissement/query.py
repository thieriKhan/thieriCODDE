from django.contrib.auth.models import Group, User
from Etablissement.models import *
from userProfiles.models import Profile


# returns all the students
get_stud = User.objects.filter(groups__name="ETUDIANTS")

# returns all the teachers
get_teach = User.objects.filter(groups__name="ENSEIGNANTS")

# returns the profile of all students
stud_prof = []
for stp in get_stud :
    id_stud =stp.id
    p = Profile.objects.get(user=id_stud)
    stud_prof.append(p)

# returns the profile of all teachers
teach_prof = []
for tp in get_teach :
    s = Profile.objects.get(user_id=tp.id).phone_number
    teach_prof.append(s)

# returns the numbers of all the students
stud_number=[]
for us in get_stud :
    phone = Profile.objects.get(user=us.id).phone_number
    stud_number.append(phone)

# returns the numbers of all the teachers
teach_number=[]
for us in get_teach :
    phone = Profile.objects.filter(user=us.id).get().phone_number
    stud_number.append(phone)



#returns the number  of all groups name users in a departement in a departement
def phone_Dep(group_nam,id_dep):
    #return the id of the department
    stud = Profile.objects.filter(user__groups__name=group_nam).filter(departement__id=id_dep)
    
    phone_numbers = []
    for prof in stud :
        phone_numbers.append(prof.phone_number)
    return phone_numbers



#returns the number  of all group's name  in a filiere
def phone_Fi(name_goup,id_Fi):
    stud_prof=Profile.objects.filter(user__groups__name=name_goup).filter(filiere__id=id_Fi)
    phone_numbers = []
    for prof in stud_prof :
        phone_numbers.append(prof.phone_number)

    return phone_numbers

#returns the number  of all teachers in a filiere


#returns all the filieres of and departement
def get_fi(name_de):
    dep = Departement.objects.get(nom_Dep=name_de)
    fils = dep.filiere_set.all()
    return fils







