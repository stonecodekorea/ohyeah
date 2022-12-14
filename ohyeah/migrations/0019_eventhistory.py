# Generated by Django 4.0.5 on 2022-07-14 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ohyeah', '0018_booking_book_status2'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_room_number', models.CharField(max_length=10, null=True)),
                ('event_type', models.CharField(max_length=20, null=True)),
                ('event_type2', models.CharField(max_length=20, null=True)),
                ('event_info', models.CharField(max_length=20, null=True)),
                ('event_date', models.DateTimeField(null=True)),
                ('event_history_date', models.DateTimeField(null=True)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ohyeah.booking')),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ohyeah.reservation')),
            ],
        ),
    ]
