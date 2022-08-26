from dataclasses import fields
from django import forms
from .models import EventHistory, Room, TotalRoomFloor, Reservation, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("room_number","room_type","room_floor","room_visi")

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('res_name','res_room_number',
                  'res_money','res_person','res_type','res_ota','res_company',
                  'res_guest_info','res_chkin',
                  'res_chkout','res_chk_time','res_guest_phone','res_guest_type',
                  'res_cash_money','res_card_money','res_bank_money','res_misu_money','res_night')

class BookForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('book_name','book_room_number',
                  'book_money','book_person','book_type','book_ota','book_company',
                  'book_guest_info','book_chkin',
                  'book_chkout','book_chk_time','book_guest_phone','book_guest_type',
                  'book_cash_money','book_card_money','book_bank_money','book_misu_money','book_night')
    
class RoomFloorForm(forms.ModelForm):
    class Meta:
        model = TotalRoomFloor
        fields = ("room_floor_high","room_floor_low")
