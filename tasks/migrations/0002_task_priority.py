# Generated by Django 4.2.1 on 2023-05-11 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('L', 'Prioridad baja'), ('N', 'Prioridad media'), ('H', 'Prioridad alta')], default='N', max_length=1),
        ),
    ]
