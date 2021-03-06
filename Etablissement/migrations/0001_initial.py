# Generated by Django 3.1 on 2020-08-16 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Abrreviation_Dep', models.CharField(default=None, max_length=10)),
                ('nom_Dep', models.CharField(max_length=50)),
                ('image_Dep', models.ImageField(default='img/pattern.jpg', upload_to='img')),
            ],
        ),
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Abrreviation_Fi', models.CharField(default=None, max_length=10)),
                ('nom_Fi', models.CharField(max_length=50)),
                ('image_Fi', models.ImageField(default='img/img1.jpg', upload_to='img')),
                ('Departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Etablissement.departement')),
            ],
        ),
    ]
