# Generated by Django 5.0.1 on 2025-07-02 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_description', models.TextField(null=True)),
                ('category_created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('product_details', models.TextField(null=True)),
                ('product_created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ElectronicsReviewApp.category')),
            ],
        ),
    ]
