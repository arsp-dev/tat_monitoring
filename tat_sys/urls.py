from django.urls import path, re_path
from . import views


urlpatterns = [
#    re_path(r'tat_sys/batches/(?P<batch_id>\w{0,50})/$', views.batches,name="batches"),
   path('batches/<int:batch_id>/', views.batches,name="batches"),
   path('', views.tat_landing, name="tat_landing"),
   path('login',views.staff_login, name="staff_login"),
   path('logout',views.staff_logout, name="staff_logout"),
   path('save_batches', views.save_batches, name="save_batches"),
   path('edit_batches', views.edit_batches, name="edit_batches"),
   path('edit_process', views.edit_process, name="edit_process"),
   path('save_holiday', views.save_holiday, name="save_holiday"),
   path('add_process', views.add_process, name="add_process"),
   path('finish_batch', views.finish_batch, name="finish_batch"),
   path('receiving', views.receiving_view, name="receiving"),
   path('monitoring', views.monitoring_view, name="monitoring"),
   path('calendar', views.calendar_view, name="calendar"),
   path('save_package', views.save_package, name="save_package"),
   path('delete_batch', views.delete_batch, name="delete_batch"),
   path('delete_package', views.delete_package, name="delete_package"),
   path('qr-code/<str:batch_uuid>/', views.qr_code, name="qr_code"),
   path('encoding', views.encoding_view, name="encoding"),
   path('create_referred', views.create_referred, name="create_referred"),
   path('referred_list_view/<str:uuid>/', views.referred_list_view, name="referred_list_view"),
   path('referred_view/<str:uuid>/', views.referred_view, name="referred_view"),
   path('save_referred/', views.save_referred, name="save_referred"),
   path('save_referred_lab/', views.save_referred_lab, name="save_referred_lab"),
   path('update_org_code/', views.update_org_code, name="update_org_code"),
   path('generate_report/<str:uuid>/', views.generate_report, name="generate_report"),
] 