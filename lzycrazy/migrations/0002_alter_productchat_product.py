# Generated by Django 4.1.7 on 2023-06-21 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lzycrazy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productchat',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='lzycrazy.product'),
        ),
    ]
