# Generated by Django 5.0.6 on 2024-06-24 08:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=19, validators=[django.core.validators.RegexValidator(message='ISBN must be in the format XXX-XXX-XXXXX-XXX-X', regex='^\\d{3}-\\d{3}-\\d{5}-\\d{3}-\\d{1}$')])),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('published_year', models.DateField()),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
    ]