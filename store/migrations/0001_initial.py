# Generated by Django 5.0.1 on 2024-05-20 02:34

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stock', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/products')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GraphicCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('vram', models.TextField()),
                ('fanquantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('speed', models.FloatField()),
                ('coreq', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('inches', models.IntegerField(default=0)),
                ('refreshrate', models.IntegerField(default=0)),
                ('technology', models.CharField(choices=[('LED', 'LED'), ('LCD', 'LCD'), ('OLED', 'OLED')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField(default=520)),
                ('technology', models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('M.2', 'M.2')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
            ],
            bases=('store.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='graphicscard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.graphiccard'),
        ),
        migrations.AddField(
            model_name='product',
            name='processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.processor'),
        ),
        migrations.AddField(
            model_name='product',
            name='ram',
            field=models.ManyToManyField(to='store.ram'),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comments', models.TextField()),
                ('address', models.TextField()),
                ('status', models.CharField(choices=[('P', 'PENDIENTE'), ('E', 'ENVIADO'), ('R', 'RECIBIDO')], default='P', max_length=1)),
                ('recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='storage',
            field=models.ManyToManyField(to='store.storage'),
        ),
        migrations.CreateModel(
            name='AllInOne',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
                ('screen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.screen')),
            ],
            bases=('store.product',),
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
                ('screen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.screen')),
            ],
            bases=('store.product',),
        ),
    ]
