# Generated by Django 4.0.5 on 2022-07-27 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohyeah', '0020_booking_book_night_reservation_res_night'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='book_chkin2',
            field=models.DateField(null=True),
        ),
    ]
