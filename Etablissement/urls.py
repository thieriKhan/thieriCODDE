from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
	path('departement/<int:id_dep>',views.sendDepartement,name="departement"),
	path('departement/filiere/<int:id_fi>',views.sendFiliere,name="filiere"),
	path('profile/', views.update_profile,name="myProfile"),
	path('welcome/', views.welcome, name='welcome'),

	path('profile/ajax/load-filiere/', views.load_filieres, name='ajax_load_filieres'),  # AJAX
	


]