from asyncio.windows_events import NULL
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests, json
from selenium import webdriver

from .forms import RoomForm, ReservationForm, BookForm
from .models import EventHistory, Room, Reservation, Booking
# Create your views here.

@login_required(login_url='common/login')
def index(request):
    room_list = Room.objects.order_by('-room_floor','room_number')
    current_date = DateFormat(datetime.now()).format('Y-m-d')
    status_date = request.GET.get('res_date',current_date)
    status_date_data = status_date.format('Ymd')
    res_list = Reservation.objects.order_by('-res_room_number','res_type','-res_chkin').filter(Q(res_chkin__lte=status_date)&Q(res_chkout__gte=status_date))
    #book_list = Booking.objects.order_by('-book_room_number','book_type','-book_chkin').filter(Q(book_chkin__lte=status_date)&Q(book_chkout__gte=status_date))
    book_list = Booking.objects.order_by('-book_room_number','book_type','-book_chkin').filter(Q(book_chkin2__icontains=status_date))
    event_obj = get_room_event(status_date)
    res_done_list = event_obj['res_done_list']
    res_not_yet_list = event_obj['res_not_yet_list']
    book_rent_done_list = event_obj['book_rent_done_list']
    book_stay_done_list = event_obj['book_stay_done_list']
    book_out_list = event_obj['book_out_list']
    book_cleaned_list = event_obj['book_cleaned_list']
    res_not_yet_rent_list = event_obj['res_not_yet_rent_list']
    res_not_yet_stay_list = event_obj['res_not_yet_stay_list']
    context = {'room_list':room_list, 'res_list':res_list,'book_list':book_list, 'status_date':status_date,
               'res_done_list':res_done_list, 'res_not_yet_list':res_not_yet_list, 'book_rent_done_list':book_rent_done_list, 'book_stay_done_list':book_stay_done_list,
               'book_out_list':book_out_list, 'book_cleaned_list':book_cleaned_list,'res_not_yet_rent_list':res_not_yet_rent_list,
               'res_not_yet_stay_list':res_not_yet_stay_list, 'event_obj':event_obj}
    return render(request, 'ohyeah/room_status.html', context)

@login_required(login_url='common/login')
def daily_report(request):
    current_date = DateFormat(datetime.now()).format('Y-m-d')
    status_date = request.GET.get('res_date',current_date)
    status_date_data = status_date.format('Ymd')
    book_list = Booking.objects.order_by('-book_room_number','book_type','-book_chkin').filter(Q(book_chkin2__icontains=status_date))
    
    rent_list = book_list.filter(book_type__icontains='rent')
    rent_count = book_list.filter(book_type__icontains='rent').count()
    rent_kiosk_list = book_list.filter(Q(book_type__icontains='rent')&Q(book_ota__icontains='kiosk'))
    rent_kiosk_cash_amount = rent_kiosk_list.aggregate(Sum('book_cash_money'))
    rent_kiosk_cash_count = rent_kiosk_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    rent_walkin_list = book_list.filter(Q(book_type__icontains='rent')&(Q(book_ota__icontains='walkin')|Q(book_ota__icontains='calling')))
    rent_walkin_cash_amount = rent_walkin_list.aggregate(Sum('book_cash_money'))
    rent_walkin_card_amount = rent_walkin_list.aggregate(Sum('book_card_money'))
    rent_walkin_bank_amount = rent_walkin_list.aggregate(Sum('book_bank_money'))
    rent_walkin_misu_amount = rent_walkin_list.aggregate(Sum('book_misu_money'))
    rent_walkin_cash_count = rent_walkin_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    rent_walkin_card_count = rent_walkin_list.filter(book_card_money__gt=0).annotate(Count('book_card_money'))
    rent_walkin_bank_count = rent_walkin_list.filter(book_bank_money__gt=0).annotate(Count('book_bank_money'))
    rent_walkin_misu_count = rent_walkin_list.filter(book_misu_money__gt=0).annotate(Count('book_misu_money'))
    rent_walkin_total_money = rent_walkin_list.aggregate(Sum('book_money'))
    rent_yanolja_list = book_list.filter(Q(book_type__icontains='rent')&Q(book_ota__icontains='yanolja'))
    rent_yanolja_total_amount = rent_yanolja_list.aggregate(Sum('book_money'))
    rent_yanolja_total_count = rent_yanolja_list.filter(book_money__gt=0).annotate(Count('book_money'))
    
    rent_cash_total_money = rent_list.aggregate(Sum('book_cash_money'))
    rent_total_money = rent_list.aggregate(Sum('book_money'))
    
    rent_walkin_c = rent_list.filter(book_guest_type__icontains='wic')
    rent_walkin_b = rent_list.filter(book_guest_type__icontains='wib')
    rent_walkin_f = rent_list.filter(book_guest_type__icontains='wif')
    rent_online_c = rent_list.filter(book_guest_type__icontains='onc')
    rent_online_b = rent_list.filter(book_guest_type__icontains='onb')
    rent_online_f = rent_list.filter(book_guest_type__icontains='onf')
    rent_kiosk = rent_list.filter(book_guest_type__icontains='kioskguest')
    
    stay_count = book_list.filter(book_type__icontains='stay').count()
    stay_list = book_list.filter(book_type__icontains='stay')
    stay_sev_count = book_list.filter(Q(book_type__icontains='stay')&Q(book_night__gt=1)).count()
    stay_sev_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_night__gt=1))
    stay_kiosk_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='kiosk'))
    stay_kiosk_cash_amount = stay_kiosk_list.aggregate(Sum('book_cash_money'))
    stay_kiosk_cash_count = stay_kiosk_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    
    stay_walkin_c = stay_list.filter(book_guest_type__icontains='wic')
    stay_walkin_b = stay_list.filter(book_guest_type__icontains='wib')
    stay_walkin_f = stay_list.filter(book_guest_type__icontains='wif')
    stay_online_c = stay_list.filter(book_guest_type__icontains='onc')
    stay_online_b = stay_list.filter(book_guest_type__icontains='onb')
    stay_online_f = stay_list.filter(book_guest_type__icontains='onf')
    stay_kiosk = stay_list.filter(book_guest_type__icontains='kioskguest')
    
    stay_walkin_list = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='walkin')|Q(book_ota__icontains='calling'))).filter(book_night__lte=1)
    stay_sev_walkin_list = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='walkin')|Q(book_ota__icontains='calling'))).filter(book_night__gt=1)
    stay_walkin_cash_amount = stay_walkin_list.aggregate(Sum('book_cash_money'))
    stay_walkin_card_amount = stay_walkin_list.aggregate(Sum('book_card_money'))
    stay_walkin_bank_amount = stay_walkin_list.aggregate(Sum('book_bank_money'))
    stay_walkin_misu_amount = stay_walkin_list.aggregate(Sum('book_misu_money'))
    stay_walkin_total_money = stay_walkin_list.aggregate(Sum('book_money'))
    stay_walkin_cash_count = stay_walkin_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    stay_walkin_card_count = stay_walkin_list.filter(book_card_money__gt=0).annotate(Count('book_card_money'))
    stay_walkin_bank_count = stay_walkin_list.filter(book_bank_money__gt=0).annotate(Count('book_bank_money'))
    stay_walkin_misu_count = stay_walkin_list.filter(book_misu_money__gt=0).annotate(Count('book_misu_money'))
    
    stay_sev_walkin_cash_amount = stay_sev_walkin_list.aggregate(Sum('book_cash_money'))
    stay_sev_walkin_card_amount = stay_sev_walkin_list.aggregate(Sum('book_card_money'))
    stay_sev_walkin_bank_amount = stay_sev_walkin_list.aggregate(Sum('book_bank_money'))
    stay_sev_walkin_misu_amount = stay_sev_walkin_list.aggregate(Sum('book_misu_money'))
    stay_sev_walkin_total_money = stay_sev_walkin_list.aggregate(Sum('book_money'))
    stay_sev_walkin_cash_count = stay_sev_walkin_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    stay_sev_walkin_card_count = stay_sev_walkin_list.filter(book_card_money__gt=0).annotate(Count('book_card_money'))
    stay_sev_walkin_bank_count = stay_sev_walkin_list.filter(book_bank_money__gt=0).annotate(Count('book_bank_money'))
    stay_sev_walkin_misu_count = stay_sev_walkin_list.filter(book_misu_money__gt=0).annotate(Count('book_misu_money'))
    
    stay_yanolja_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='yanolja')&Q(book_night__lte=1))
    stay_yanolja_total_amount = stay_yanolja_list.aggregate(Sum('book_money'))
    stay_yanolja_total_count = stay_yanolja_list.filter(book_money__gt=0).annotate(Count('book_money'))
    stay_sev_yanolja_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='yanolja')&Q(book_night__gt=1)&Q(book_chkin2__gt=status_date))
    stay_sev_yanolja_total_amount = stay_yanolja_list.aggregate(Sum('book_money'))
    stay_sev_yanolja_total_count = stay_yanolja_list.filter(book_money__gt=0).annotate(Count('book_money'))
    
    stay_hotelstory_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='hotelstory')&Q(book_night__lte=1))
    stay_hotelstory_total_amount = stay_hotelstory_list.aggregate(Sum('book_money'))
    stay_hotelstory_total_count = stay_hotelstory_list.filter(book_money__gt=0).annotate(Count('book_money'))
    stay_sev_hotelstory_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='hotelstory')&Q(book_night__lte=1)&Q(book_chkin2__gt=status_date))
    stay_sev_hotelstory_total_amount = stay_hotelstory_list.aggregate(Sum('book_money'))
    stay_sev_hotelstory_total_count = stay_hotelstory_list.filter(book_money__gt=0).annotate(Count('book_money'))
    
    stay_naver_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='naver')&Q(book_night__lte=1))
    stay_naver_total_amount = stay_naver_list.aggregate(Sum('book_money'))
    stay_naver_total_count = stay_naver_list.filter(book_money__gt=0).annotate(Count('book_money'))
    stay_sev_naver_list = book_list.filter(Q(book_type__icontains='stay')&Q(book_ota__icontains='naver')&Q(book_night__gt=1)&Q(book_chkin2__gt=status_date))
    stay_sev_naver_total_amount = stay_naver_list.aggregate(Sum('book_money'))
    stay_sev_naver_total_count = stay_naver_list.filter(book_money__gt=0).annotate(Count('book_money'))
    
    
    stay_online_total_count = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver'))).filter(book_night__lte=1).filter(book_money__gt=0).annotate(Count('book_money'))
    stay_online_total_amount = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver'))).filter(book_night__lte=1).aggregate(Sum('book_money'))
    stay_sev_online_total_count = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver'))).filter(book_night__gt=1).filter(book_money__gt=0).annotate(Count('book_money'))
    stay_sev_online_total_amount = book_list.filter(Q(book_type__icontains='stay')&(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver'))).filter(book_night__gt=1).aggregate(Sum('book_money'))
    total_card_count = book_list.filter(book_card_money__gt=0).annotate(Count('book_card_money'))
    total_cash_count = book_list.filter(book_cash_money__gt=0).annotate(Count('book_cash_money'))
    total_bank_count = book_list.filter(book_bank_money__gt=0).annotate(Count('book_bank_money'))
    total_misu_count = book_list.filter(book_misu_money__gt=0).annotate(Count('book_misu_money'))
    total_online_count = book_list.filter(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver')).filter(book_money__gt=0).annotate(Count('book_money'))
    total_card_sum = book_list.aggregate(Sum('book_card_money'))
    total_cash_sum = book_list.aggregate(Sum('book_cash_money'))
    total_bank_sum = book_list.aggregate(Sum('book_bank_money'))
    total_misu_sum = book_list.aggregate(Sum('book_misu_money'))
  
    stay_cash_money_total = stay_list.aggregate(Sum('book_cash_money'))
    stay_sev_cash_money_total = stay_sev_list.aggregate(Sum('book_cash_money'))
    
    
    if stay_cash_money_total['book_cash_money__sum'] is None:
        stay_cash_money_total = 0
    else:
        stay_cash_money_total = stay_cash_money_total['book_cash_money__sum']
    if stay_sev_cash_money_total['book_cash_money__sum'] is None:
        stay_sev_cash_money_total = 0
    else:
        stay_sev_cash_money_total = stay_sev_cash_money_total['book_cash_money__sum']    
        
        
    if rent_cash_total_money['book_cash_money__sum'] is None:
        rent_cash_total_money = 0
    else:
        rent_cash_total_money = rent_cash_total_money['book_cash_money__sum']

    
    book_stay_money_total = rent_cash_total_money+stay_cash_money_total
    
    stay_total_money = stay_list.aggregate(Sum('book_money'))
    stay_sev_total_money = stay_sev_list.aggregate(Sum('book_money'))
    

    total_online_sum = book_list.filter(Q(book_ota__icontains='yanolja')|Q(book_ota__icontains='hotelstory')|Q(book_ota__icontains='naver')).aggregate(Sum('book_money'))
    
    rent_type = {'rent_walkin_c':rent_walkin_c,'rent_walkin_b':rent_walkin_b,'rent_walkin_f':rent_walkin_f,'rent_online_c':rent_online_c,
                 'rent_online_b':rent_online_b,'rent_online_f':rent_online_f,'rent_kiosk':rent_kiosk}
    
    stay_type = {'stay_walkin_c':stay_walkin_c,'stay_walkin_b':stay_walkin_b,'stay_walkin_f':stay_walkin_f,'stay_online_c':stay_online_c,
                 'stay_online_b':stay_online_b,'stay_online_f':stay_online_f,'stay_kiosk':stay_kiosk}
    
    stay_sev_obj = {'stay_sev_walkin_cash_amount':stay_sev_walkin_cash_amount,'stay_sev_walkin_card_amount':stay_sev_walkin_card_amount,'stay_sev_walkin_bank_amount':stay_sev_walkin_bank_amount
                    ,'stay_sev_walkin_misu_amount':stay_sev_walkin_misu_amount,'stay_sev_walkin_total_money':stay_sev_walkin_total_money,'stay_sev_walkin_cash_count':stay_sev_walkin_cash_count,
                    'stay_sev_walkin_card_count':stay_sev_walkin_card_count,'stay_sev_walkin_bank_count':stay_sev_walkin_bank_count,'stay_sev_walkin_misu_count':stay_sev_walkin_misu_count,
                    'stay_sev_yanolja_total_amount':stay_sev_yanolja_total_amount,'stay_hotelstory_total_count':stay_hotelstory_total_count,'stay_sev_hotelstory_total_amount':stay_sev_hotelstory_total_amount
                    ,'stay_sev_hotelstory_total_count':stay_sev_hotelstory_total_count,'stay_sev_naver_total_amount':stay_sev_naver_total_amount,'stay_sev_naver_total_count':stay_sev_naver_total_count,
                    'stay_sev_online_total_count':stay_sev_online_total_count,'stay_sev_online_total_amount':stay_sev_online_total_amount,'stay_sev_count':stay_sev_count,'stay_sev_total_money':stay_sev_total_money}
    
    context = {'status_date':status_date, 'book_list':book_list, 'rent_kiosk_list':rent_kiosk_list, 'rent_walkin_list':rent_walkin_list,'rent_yanolja_list':rent_yanolja_list,
               'rent_kiosk_cash_amount':rent_kiosk_cash_amount, 'rent_kiosk_cash_count':rent_kiosk_cash_count,'rent_yanolja_total_amount':rent_yanolja_total_amount,
               'rent_yanolja_total_count':rent_yanolja_total_count,'rent_walkin_cash_amount':rent_walkin_cash_amount,'rent_walkin_card_amount':rent_walkin_card_amount,
               'rent_walkin_bank_amount':rent_walkin_bank_amount,'rent_walkin_misu_amount':rent_walkin_misu_amount,'rent_walkin_cash_count':rent_walkin_cash_count,
               'rent_walkin_card_count':rent_walkin_card_count,'rent_walkin_bank_count':rent_walkin_bank_count,'rent_walkin_misu_count':rent_walkin_misu_count,'rent_count':rent_count,
               'stay_count':stay_count,'stay_kiosk_cash_amount':stay_kiosk_cash_amount,'stay_kiosk_cash_count':stay_kiosk_cash_count,'stay_kiosk_list':stay_kiosk_list,
               'stay_walkin_list':stay_walkin_list,'stay_walkin_cash_amount':stay_walkin_cash_amount,'stay_walkin_card_amount':stay_walkin_card_amount,'stay_walkin_bank_amount':stay_walkin_bank_amount,
               'stay_walkin_misu_amount':stay_walkin_misu_amount,'stay_walkin_cash_count':stay_walkin_cash_count,'stay_walkin_card_count':stay_walkin_card_count,
               'stay_walkin_bank_count':stay_walkin_bank_count,'stay_walkin_misu_count':stay_walkin_misu_count,'stay_yanolja_list':stay_yanolja_list,
               'stay_yanolja_total_amount':stay_yanolja_total_amount,'stay_yanolja_total_count':stay_yanolja_total_count,'stay_hotelstory_list':stay_hotelstory_list,
               'stay_hotelstory_total_amount':stay_hotelstory_total_amount,'stay_hotelstory_total_count':stay_hotelstory_total_count,'stay_naver_list':stay_naver_list,
               'stay_naver_total_amount':stay_naver_total_amount,'stay_naver_total_count':stay_naver_total_count,'stay_online_total_amount':stay_online_total_amount,
               'total_card_count':total_card_count,'total_cash_count':total_cash_count,'total_bank_count':total_bank_count,'total_misu_count':total_misu_count,
               'total_online_count':total_online_count,'total_card_sum':total_card_sum,'total_cash_sum':total_cash_sum,'total_bank_sum':total_bank_sum,'total_misu_sum':total_misu_sum,
               'total_online_sum':total_online_sum,'stay_online_total_count':stay_online_total_count, 'stay_walkin_total_money':stay_walkin_total_money,
               'rent_walkin_total_money':rent_walkin_total_money,'rent_cash_total_money':rent_cash_total_money,'rent_total_money':rent_total_money,'stay_total_money':stay_total_money,
               'book_stay_money_total':book_stay_money_total,'stay_sev_obj':stay_sev_obj, 'rent_type':rent_type, 'stay_type':stay_type}
    return render(request, 'ohyeah/daily_report.html', context)

@login_required(login_url='common/login')
def month_report(request):
    current_date = DateFormat(datetime.now()).format('Y-m')
    status_date = request.GET.get('res_date',current_date)
    context = {'status_date':status_date}
    return render(request, 'ohyeah/month_report.html', context)


@login_required(login_url='common/login')
def get_event_view(request, current_date, category):
    if current_date is not None:
        cur_date = current_date
    else :
        cur_date = DateFormat(datetime.now()).format('Y-m-d')
    if category is not None:
        cat = category
    else :
        cat = 'book_out'
    status_date = cur_date
    status_category = cat
    event_obj = get_room_event(current_date)    
    context = {'event_obj':event_obj, 'status_date':status_date, 'status_category':status_category}
    return render(request, 'ohyeah/event_status.html', context)

@login_required(login_url='common/login')
def event_list(request):
    current_date = DateFormat(datetime.now()).format('Y-m-d')
    status_date = request.GET.get('res_date',current_date)
    status_date_data = status_date.format('Ymd')
    event_category = request.GET.get('event_category','res_done')
    event_obj = get_room_event(status_date)
    
    context = { 'status_date':status_date, 'event_category':event_category, 'event_obj':event_obj}
    return render(request, 'ohyeah/event_list.html', context)

def get_room_event(current_date):
    event_list = EventHistory.objects.filter(event_date__icontains=current_date)
    res_done_list = event_list.filter(Q(event_type__icontains='reservation')&Q(event_type2__icontains='off'))
    res_not_yet_list = event_list.filter(Q(event_type2__icontains='on')&Q(event_type__icontains='reservation'))
    res_not_yet_rent_list = event_list.filter(Q(event_type2__icontains='on')&Q(event_type__icontains='reservation')&Q(event_info__icontains='rent'))
    res_not_yet_stay_list = event_list.filter(Q(event_type2__icontains='on')&Q(event_type__icontains='reservation')&Q(event_info__icontains='stay'))
    book_rent_done_list = event_list.filter(Q(event_info__icontains='rent')&Q(event_type__icontains='booking'))
    book_stay_done_list = event_list.filter(Q(event_info__icontains='stay')&Q(event_type__icontains='booking'))
    book_out_list = event_list.filter(Q(event_type__icontains='book_out'))
    book_cleaned_list = event_list.filter(Q(event_type__icontains='clean_done'))
    event_obj = {'res_done_list':res_done_list,'res_not_yet_list':res_not_yet_list,'book_rent_done_list':book_rent_done_list,'book_stay_done_list':book_stay_done_list,
                 'book_out_list':book_out_list,'book_cleaned_list':book_cleaned_list,'res_not_yet_rent_list':res_not_yet_rent_list
                 ,'res_not_yet_stay_list':res_not_yet_stay_list}
    return event_obj

@login_required(login_url='common/login')
def res_view(request, res_id):
    reservation = get_object_or_404(Reservation, pk=res_id)
    context = {'reservation':reservation}
    return render(request, 'ohyeah/res_status.html', context)

@login_required(login_url='common/login')
def book_view(request, book_id):
    current_date = DateFormat(datetime.now()).format('Y-m-d')
    status_date = request.GET.get('res_date',current_date)
    book = get_object_or_404(Booking, pk=book_id)
    context = {'book':book,'status_date':status_date}
    return render(request, 'ohyeah/book_status.html', context)

@login_required(login_url='common/login')
def book_modify(request, book_id):
    book = get_object_or_404(Booking, pk=book_id)
    if request.method=="POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.book_modify_date = timezone.now()
            book.save()
            event_obj = {'event_type':'book_modify','event_room_number':book.book_room_number,'event_type2':'book_modify','event_info':'none','event_date':timezone.now(),'id':book.id}
            event_add(event_obj)
            return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')
    else :
        form = BookForm()
    context = {'form':book, 'book_id':book.id, 'test':form}
    return render(request, 'ohyeah/book_form.html', context)

@login_required(login_url='common/login')
def book_out(request, book_id, status_date):
    book = get_object_or_404(Booking, pk=book_id)
    book.book_status="off"
    book.save()
    event_obj = {'event_type':'book_out','event_room_number':book.book_room_number,'event_type2':'none','event_info':book.book_type,'event_date':status_date,'id':book.id}
    event_add(event_obj)
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')

@login_required(login_url='common/login')
def book_clean_done(request, book_id, status_date):
    book = get_object_or_404(Booking, pk=book_id)
    days = (book.book_chkout-book.book_chkin).days
    if days <= 1:
        book.book_status="done"
        book.book_status2="done"
        event_obj = {'event_type':'clean_done','event_room_number':book.book_room_number,'event_type2':'none','event_info':book.book_type,'event_date':status_date,'id':book.id}
        event_add(event_obj)
    else :
        book.book_status="on"
        book.book_status2="done"
        event_obj = {'event_type':'clean_done','event_room_number':book.book_room_number,'event_type2':'several_days','event_info':book.book_type,'event_date':status_date,'id':book.id}
        event_add(event_obj)
        event_obj = {'event_type':'booking','event_room_number':book.book_room_number,'event_type2':'several_days','event_info':book.book_type,'event_date':status_date,'id':book.id}
        event_add(event_obj)
    book.save()
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')

@login_required(login_url='common/login')
def book_delete(request, book_id):
    book = get_object_or_404(Booking, pk=book_id)
    book.delete()
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')

@login_required(login_url='common/login')
def res_modify(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    if request.method=="POST":
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            res.res_modify_date = timezone.now()
            res.save()
            event_obj = {'event_type':'res_modify','event_room_number':res.res_room_number,'event_type2':'res_modify','event_info':'none','event_date':timezone.now(),'id':res.id}
            event_add(event_obj)
            return redirect('ohyeah:res_status', res_id=res.id)
    else :
        form = ReservationForm()
    context = {'form':res, 'res_id':res.id, 'test':form}
    return render(request, 'ohyeah/res_form.html', context)         
          
@login_required(login_url='common/login')
def res_book(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    book = Booking(book_name=res.res_name, book_room_number=res.res_room_number,
                   book_money=res.res_money, book_cash_money=res.res_cash_money,
                   book_card_money=res.res_card_money, book_bank_money=res.res_bank_money,
                   book_misu_money=res.res_misu_money, book_person=res.res_person,
                   book_type=res.res_type, book_ota=res.res_ota,
                   book_company=res.res_company, book_payment_info=res.res_payment_info,
                   book_guest_info=res.res_guest_info, book_guest_type=res.res_guest_type,
                   book_guest_phone=res.res_guest_phone, book_chkin=res.res_chkin,
                   book_chkout=res.res_chkout, book_chk_time=res.res_chk_time,
                   book_date=res.res_date, book_status='on')
    res.res_status="off"
    res.save()
    book.save()
    event_obj = {'event_type':'booking','event_room_number':book.book_room_number,'event_type2':'none','event_info':res.res_type,'event_date':res.res_chkin,'id':book.id}
    event_add(event_obj)
    event_obj = EventHistory.objects.filter(Q(event_type__icontains='reservation')&Q(event_date__contains=res.res_date))
    event_obj.event_type2='off'
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')
  
@login_required(login_url='common/login')
def res_delete(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    res.delete()
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.location.reload();</script>')

@login_required(login_url='common/login')
def room_add(request):
    form = RoomForm(request.POST)
    if request.method=="POST":
        if form.is_valid():    
            room = form.save(commit=False)
            form.save()
            return render(request,'ohyeah/room_add.html')
    else:
        form = RoomForm()
    return render(request, 'ohyeah/room_add.html', {'form':form})

@login_required(login_url='common/login')
def res_add(request):
    form = ReservationForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            res = form.save(commit=False)
            res.res_date = timezone.now()
            res.res_status="on"
            form.save()
            event_obj = {'event_type':'reservation','event_room_number':res.res_room_number,'event_type2':'none','event_info':res.res_type,'event_date':res.res_chkin,'id':res.id}
            event_add(event_obj)
            return redirect('ohyeah:index')
    else:
        form = ReservationForm(request.POST)
    return render(request, 'ohyeah/res_add.html', {'form':form})

@login_required(login_url='common/login')
def book_add(request):
    form = BookForm(request.POST)
    night = int(request.POST.get('book_night'))
    
    if request.method=="POST":
        
        if form.is_valid():
            
            if night > 1:
                chkin = request.POST.get('book_chkin')
                for i in range(night):

                    next_chkin = datetime.strftime(datetime.strptime(chkin, "%Y-%m-%d")+timedelta(days=i),'%Y-%m-%d')
                    book = Booking(book_room_number=form.cleaned_data['book_room_number'],book_name=form.cleaned_data['book_name'],book_money=form.cleaned_data['book_money'],
                                   book_cash_money=form.cleaned_data['book_cash_money'], book_card_money=form.cleaned_data['book_card_money'], book_bank_money=form.cleaned_data['book_bank_money'],
                                   book_misu_money=form.cleaned_data['book_misu_money'], book_person=form.cleaned_data['book_person'], book_type=form.cleaned_data['book_type'],
                                   book_ota=form.cleaned_data['book_ota'], book_company=form.cleaned_data['book_company'],book_guest_info=form.cleaned_data['book_guest_info'],
                                   book_guest_type=form.cleaned_data['book_guest_type'],book_guest_phone=form.cleaned_data['book_guest_phone'],book_chkin2=next_chkin,book_chkin=form.cleaned_data['book_chkin'],
                                   book_chkout=form.cleaned_data['book_chkout'], book_chk_time=form.cleaned_data['book_chk_time'],book_date=timezone.now(), 
                                   book_status="on", book_night=i+1)
                    book.save()
                    event_obj = {'event_type':'booking','event_room_number':book.book_room_number,'event_type2':'none','event_info':book.book_type,'event_date':next_chkin,'id':book.id}
                    event_add(event_obj)
            else :
                book = form.save(commit=False)
                book.book_status = "on"
                book.book_date = timezone.now()
                book.book_chkin2 = form.cleaned_data['book_chkin']
                form.save()
                event_obj = {'event_type':'booking','event_room_number':book.book_room_number,'event_type2':'none','event_info':book.book_type,'event_date':book.book_chkin,'id':book.id}
                event_add(event_obj)
            return redirect('ohyeah:index')
    else:
        form = BookForm(request.POST)
    return render(request, 'ohyeah/book_add.html', {'form':form})

def event_add(event_obj):
    res = None
    book = None
    event_history = EventHistory(event_room_number=event_obj['event_room_number'],
    event_type=event_obj['event_type'], event_type2=event_obj['event_type2'],
    event_info=event_obj['event_info'], event_date=event_obj['event_date'],
    event_history_date=timezone.now())
    
    if event_obj['event_type'] == 'reservation':
        res = get_object_or_404(Reservation, pk=event_obj['id'])    
        event_history.reservation = res
    elif event_obj['event_type'] == 'res_modify':
        res = get_object_or_404(Reservation, pk=event_obj['id'])    
        event_history.reservation = res
    elif event_obj['event_type'] == "clean_done" or event_obj['event_type'] == "book_out":
        book = get_object_or_404(Booking, pk=event_obj['id'])    
        event_history.booking = book
    elif event_obj['event_type'] == 'booking':
        book = get_object_or_404(Booking, pk=event_obj['id'])
        event_history.booking = book    
    elif event_obj['event_type'] == 'book_modify':
        book = get_object_or_404(Booking, pk=event_obj['id'])
        event_history.booking = book        
    event_history.save()
    return True
        
def login_yanolja(request):
    driver = webdriver.Chrome()
    url = 'https://www.google.com'
    driver.get(url)
    context = {'result':result}
    return render(request, 'ohyeah/yanolja_test.html', context)