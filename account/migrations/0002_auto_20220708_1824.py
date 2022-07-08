# Generated by Django 3.2.14 on 2022-07-08 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdraw',
            name='user',
        ),
        migrations.AlterField(
            model_name='transfer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.FloatField(max_length=11, unique=True, verbose_name='phone number'),
        ),
    ]
