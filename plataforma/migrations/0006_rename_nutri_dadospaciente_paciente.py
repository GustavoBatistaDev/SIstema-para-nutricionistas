# Generated by Django 3.2.15 on 2022-09-12 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0005_auto_20220912_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dadospaciente',
            old_name='nutri',
            new_name='paciente',
        ),
    ]