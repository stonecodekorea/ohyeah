from django.urls import path

from . import views

app_name = 'ohyeah'

urlpatterns = [
    path('', views.index, name='index'),
    path('room_add/', views.room_add, name='room_add'),
    path('res_add/', views.res_add, name='res_add'),
    path('res_status/<int:res_id>', views.res_view, name='res_status'),
    path('res_modify/<int:res_id>', views.res_modify, name='res_modify'),
    path('res_delete/<int:res_id>', views.res_delete, name='res_delete'),
    path('res_book/<int:res_id>', views.res_book, name='res_book'),
    path('book_add', views.book_add, name='book_add'),
    path('book_out/<int:book_id>/<str:status_date>/', views.book_out, name='book_out'),
    path('book_clean_done/<int:book_id>/<str:status_date>/', views.book_clean_done, name='book_clean_done'),
    path('book_status/<int:book_id>', views.book_view, name='book_status'),
    path('book_modify/<int:book_id>', views.book_modify, name='book_modify'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('event_status/<str:current_date>/<str:category>', views.get_event_view, name='event_status'),
    path('event_list/', views.event_list, name='event_list'),
    path('daily_report/', views.daily_report, name='daily_report'),
    path('month_report/', views.month_report, name='month_report'),
    path('yanolja_test/', views.login_yanolja, name='yanolja_test'),
]
