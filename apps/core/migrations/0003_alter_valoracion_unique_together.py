# Generated by Django 5.1.4 on 2024-12-16 16:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_receta_imagen'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='valoracion',
            unique_together={('usuario', 'receta')},
        ),
    ]
