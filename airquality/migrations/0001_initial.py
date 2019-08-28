# Generated by Django 2.2.4 on 2019-08-20 16:01

import airquality.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=5, validators=[airquality.models.validate_zipcode])),
                ('start_date', models.DateField(validators=[airquality.models.validate_date_in_range])),
                ('end_date', models.DateField(validators=[airquality.models.validate_date_in_range])),
                ('datetime_created', models.DateTimeField(verbose_name='Report Creation Date')),
            ],
        ),
    ]
