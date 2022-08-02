# Generated by Django 4.0.5 on 2022-07-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohyeah', '0005_reservation_res_chk_time_reservation_res_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='book_room_chkin_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='book_room_chkout_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_chkin_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='res_chkout_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_cancel',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_chk_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_company',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_guest_info',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_guest_phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_guest_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_money',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_number',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_payment_info',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='book_room_person',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_money',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_payment_info',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_person',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='res_type',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
