# Generated by Django 5.0.1 on 2024-06-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_recipedetails_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('T', 'TRANSFERENCIA'), ('C', 'CREDITO'), ('D', 'DEBITO'), ('CC', 'CREDITO A CUOTAS')], max_length=2),
        ),
    ]