# Generated by Django 4.2.1 on 2023-05-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_subject_options_alter_task_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='completada'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=120, unique=True, verbose_name='nombre de la asignatura'),
        ),
    ]
