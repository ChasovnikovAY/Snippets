# Generated by Django 4.1.7 on 2024-10-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_alter_snippet_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='lang',
            field=models.CharField(choices=[('py', 'Python'), ('js', 'JavaScript')], max_length=30),
        ),
    ]
