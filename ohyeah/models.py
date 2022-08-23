from django.db import models

# Create your models here.
class Room(models.Model):
    room_number = models.CharField( max_length=5)
    room_type = models.CharField(max_length=10)
    room_floor = models.CharField(max_length=3)
    room_visi = models.CharField( max_length=5)
    
class Booking(models.Model):
    book_number = models.IntegerField(null=True)
    book_name = models.CharField(max_length=50,null=True)
    book_room_number = models.CharField(max_length=10, null=True)
    book_money = models.IntegerField(null=True)
    book_cash_money = models.IntegerField(null=True)
    book_card_money = models.IntegerField(null=True)
    book_bank_money = models.IntegerField(null=True)
    book_misu_money = models.IntegerField(null=True)
    book_person = models.CharField(max_length=5, null=True)
    book_type = models.CharField(max_length=5, null=True)
    book_ota = models.CharField(max_length=10, null=True)
    book_company = models.CharField(max_length=50, null=True)
    book_payment_info = models.CharField(max_length=50, null=True)
    book_guest_info = models.TextField(null=True)
    book_guest_type = models.CharField(max_length=10, null=True)
    book_guest_phone = models.CharField(max_length=50, null=True)
    book_chkin = models.DateField(null=True)
    book_chkin2 = models.DateField(null=True)
    book_chkout = models.DateField(null=True) 
    book_chk_time = models.TimeField(null=True)
    book_date = models.DateTimeField(null=True)
    book_modify_date = models.DateTimeField(null=True)
    book_status = models.CharField(max_length=5, null=True)
    book_status2 = models.CharField(max_length=5, null=True)
    book_night = models.IntegerField(null=True)
    
class TotalRoomFloor(models.Model):
    room_floor_high = models.IntegerField()
    room_floor_low = models.IntegerField()  
    
class Reservation(models.Model):
    res_name = models.CharField(max_length=50,null=True)
    res_room_number = models.CharField(max_length=10, null=True)
    res_money = models.IntegerField(null=True)
    res_cash_money = models.IntegerField(null=True)
    res_card_money = models.IntegerField(null=True)
    res_bank_money = models.IntegerField(null=True)
    res_misu_money = models.IntegerField(null=True)
    res_person = models.CharField(max_length=5, null=True)
    res_type = models.CharField(max_length=5, null=True)
    res_ota = models.CharField(max_length=10, null=True)
    res_company = models.CharField(max_length=50, null=True)
    res_payment_info = models.CharField(max_length=50, null=True)
    res_guest_info = models.TextField(null=True)
    res_guest_type = models.CharField(max_length=10, null=True)
    res_guest_phone = models.CharField(max_length=50, null=True)
    res_chkin = models.DateField(null=True)
    res_chkout = models.DateField(null=True) 
    res_chk_time = models.TimeField(null=True)
    res_date = models.DateTimeField(null=True)
    res_modify_date = models.DateTimeField(null=True)
    res_status = models.CharField(max_length=5, null=True)
    res_night = models.IntegerField(null=True)

class EventHistory(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    event_room_number = models.CharField(max_length=10, null=True)
    event_type = models.CharField(max_length=20, null=True)
    event_type2 = models.CharField(max_length=20, null=True)
    event_info = models.CharField(max_length=20, null=True)
    event_date = models.DateTimeField(null=True)
    event_history_date = models.DateTimeField(null=True)
    



