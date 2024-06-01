# Generated by Django 5.0.1 on 2024-05-30 17:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_delivery_recipe_alter_payment_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date_paid',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='comments',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
