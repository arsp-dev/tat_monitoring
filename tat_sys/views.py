from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import datetime
from datetime import timedelta
from tat_sys.models import Batches, Holiday, Process, Packages
from django.db import IntegrityError
import os
import pandas as pd
import numpy as np
# Create your views here.
dirpath = os.getcwd()

lab_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Lab')
dmu_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Dmu')
sec_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Secretariat')

lab_staff = lab_staff['Staff Name'].values.tolist()
dmu_staff = dmu_staff['Staff Name'].values.tolist()
sec_staff = sec_staff['Staff Name'].values.tolist()


@login_required(login_url='/tat_sys/login')
def receiving_view(request):
    packages = Packages.objects.all().order_by('-created_at')
    return render(request, 'tat_sys/receiving.html',{'packages': packages,'lab_staff':lab_staff,'dmu_staff':dmu_staff,'sec_staff':sec_staff})



@login_required(login_url='/tat_sys/login')
def monitoring_view(request):
    batches = Batches.objects.all().order_by('-created_at')
    return render(request, 'tat_sys/monitoring.html',{'batches': batches,'lab_staff':lab_staff,'dmu_staff':dmu_staff,'sec_staff':sec_staff})


@login_required(login_url='/tat_sys/login')
def calendar_view(request):
    holidays = Holiday.objects.all().order_by('holiday')
    return render(request, 'tat_sys/calendar.html',{'holidays': holidays})


@login_required(login_url='/tat_sys/login')
def delete_batch(request):
    batch_id = request.POST['batch_id']
    Batches.objects.filter(process__batch_id=batch_id).delete()

    return HttpResponseRedirect('/tat_sys/monitoring')


@login_required(login_url='/tat_sys/login')
def delete_package(request):
    package_id = request.POST['package_id']
    Packages.objects.filter(id=package_id).delete()

    return HttpResponseRedirect('/tat_sys/receiving')


# GET : view for landing page
@login_required(login_url='/tat_sys/login')
def tat_landing(request):
    on_going_tat = Batches.objects.filter(date_received__gt=datetime.datetime.now() - timedelta(days=40)).filter(status=None).count()
# on_going_tat = Batches.dashboard.count()
    warning_tat = Batches.objects.filter(date_received__lt=datetime.datetime.now() - timedelta(days=40)).filter(date_received__gt=datetime.datetime.now() - timedelta(days=50)).count()
    overdue_tat = Batches.objects.filter(status='Overdue').count()
    ontime_tat = Batches.objects.filter(status='Completed').count()
    batches = Batches.objects.filter(status=None)
    
    
    processing = 0
    encoding = 0
    editing = 0
    lab_verify = 0
    final_verify = 0
    releasing = 0
    
    
    for batch in batches:
        if batch.get_current_status == 'Processing':
            processing += 1
        elif batch.get_current_status == 'Encoding':
            encoding += 1
        elif batch.get_current_status == 'Editing':
            editing += 1
        elif batch.get_current_status == 'Lab Verification':
            lab_verify += 1
        elif batch.get_current_status == 'Final Verification':
            final_verify += 1  
        elif batch.get_current_status == 'Releasing':
            releasing += 1
    

    return render(request, 'tat_sys/tat_landing.html',{'batches': batches, 'on_going_tat': on_going_tat,
                                                       'warning_tat':warning_tat,'overdue_tat':overdue_tat,
                                                       'ontime_tat':ontime_tat,'processing' : processing, 'encoding' : encoding, 'editing' : editing, 'lab_verify' : lab_verify,
                                                       'final_verify' : final_verify, 'releasing' : releasing})
# end view for landing page


# <! --- staff login and logout --- !>
def staff_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
             if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/tat_sys')
        else:
            return render(request, 'tat_sys/staff_login.html',{'error':'User not found.'})

     else:
        return render(request, 'tat_sys/staff_login.html')
    

def staff_logout(request):
    logout(request)
    return HttpResponseRedirect('/tat_sys/login')
# <! --- end of staff login and logout --!>

# <! -- save batches --!>
@login_required(login_url='/tat_sys/login')
def save_batches(request):
    if request.method == 'POST':
        site = request.POST['site']
        accession_number = request.POST['accession_number']
        isolate_number = request.POST['isolate_number']
        total_isolate_number = request.POST['total_isolate_number']
        batch_number = request.POST['batch_number']
        total_batch_number = request.POST['total_batch_number']
        date_received = request.POST['date_received']
        datereceived =  datetime.datetime.strptime(date_received, '%m/%d/%Y')
        
        date_received = date_received.replace('/','')
        start = date_received[:4]
        end = date_received[-2:]
        date_received = start + end
        
        received_by = request.POST['received_by']
        
        batch_name = site + '_' + date_received + '_' + str(batch_number) + '_' + accession_number
        
        try:
            batch = Batches.objects.create(batch_name=batch_name,
                                site=site,
                                accession_number=accession_number,
                                isolate_number=isolate_number,
                                total_isolate_number=total_isolate_number,
                                batch_number=batch_number,
                                total_batch_number=total_batch_number,
                                date_received=datereceived,
                                received_by=received_by)
            batch.process_set.create(process="1_receiving",start_date=batch.date_received)
            return HttpResponseRedirect('/tat_sys/monitoring')
        except:
            return HttpResponseRedirect('/tat_sys/monitoring')
# <! -- end batches --!>

@login_required(login_url='/tat_sys/login')
def save_package(request):
    if request.method == 'POST':
        site = request.POST['site']
        date_received = request.POST['date_received']
        datereceived =  datetime.datetime.strptime(date_received, '%m/%d/%Y')
        
        date_received = date_received.replace('/','')
        start = date_received[:4]
        end = date_received[-2:]
        date_received = start + end
        
        received_by = request.POST['received_by']
        
        package_name = site + '_' + date_received
        try:
            package = Packages.objects.create(package_name=package_name,
                                site=site,
                                date_received=datereceived,
                                received_by=received_by)
            return HttpResponseRedirect('/tat_sys/receiving')
        except:
            return HttpResponseRedirect('/tat_sys/receiving')






@login_required(login_url='/tat_sys/login')
def edit_batches(request):
    if request.method == 'POST':
        batch_id = request.POST['batch_id']
        site = request.POST['site']
        accession_number = request.POST['accession_number']
        isolate_number = request.POST['isolate_number']
        total_isolate_number = request.POST['total_isolate_number']
        batch_number = request.POST['batch_number']
        total_batch_number = request.POST['total_batch_number']
        date_received = request.POST['date_received']
        datereceived =  datetime.datetime.strptime(date_received, '%m/%d/%Y')
        
        date_received = date_received.replace('/','')
        start = date_received[:4]
        end = date_received[-2:]
        date_received = start + end
        
        # received_by = request.POST['received_by']
        
        batch_name = site + '_' + date_received + '_' + str(batch_number) + '_' + accession_number
        
       
        batch = Batches.objects.filter(id=batch_id).update(batch_name=batch_name,
                                site=site,
                                accession_number=accession_number,
                                isolate_number=isolate_number,
                                total_isolate_number=total_isolate_number,
                                batch_number=batch_number,
                                total_batch_number=total_batch_number,
                                date_received=datereceived)
        
        batch = Batches.objects.get(id=batch_id)
        return redirect('batches/' + batch_id)
# <! -- save holiday --!>
@login_required(login_url='/tat_sys/login')
def save_holiday(request):
    if request.method == 'POST':
        # print(request)
        holiday_date = request.POST['holiday_date']
        holiday_date = datetime.datetime.strptime(holiday_date, '%m/%d/%Y')
        
        chk_holiday = Holiday.objects.filter(holiday=holiday_date).count()
        
        
        try:
            if chk_holiday == 0:
                Holiday.objects.create(holiday = holiday_date)
            else:
                Holiday.objects.filter(holiday=holiday_date).delete()
                
            return HttpResponseRedirect('/tat_sys/calendar')
        except:
            return HttpResponseRedirect('/tat_sys/calendar')
        
# <! -- end holiday --!>

@login_required(login_url='/tat_sys/login')
def batches(request,batch_id):
    batch = Batches.objects.get(id=batch_id)
    # var_1_receiving = Process.objects.filter(batch__id=batch.id)
    var_1_receiving = Process.objects.filter(batch_id=batch.id).filter(process='1_receiving').get()
    # var_1_identification = Process.objects.filter(batch_id=batch.id).filter(process='1_identification').get()
   
    var_1_identification = get_variable_value(batch.id,'1_identification')
    var_2_encoding = get_variable_value(batch.id,'2_encoding')
    var_2_printing = get_variable_value(batch.id,'2_printing')
    var_3 = get_variable_many_value(batch.id,'3_')
    var_4 = get_variable_many_value(batch.id,'4_')
    var_5 = get_variable_many_value(batch.id,'5_concordance')
    var_5_1 = get_variable_many_value(batch.id,'5_1_')
    var_6 = get_variable_many_value(batch.id,'6_')
    
    # return HttpResponse(var_3)
   
    return render(request, 'tat_sys/batch_details.html',
                  {'batch': batch, 'var_1_receiving' : var_1_receiving,
                   'lab_staff' : lab_staff, 'dmu_staff' : dmu_staff, 
                   'sec_staff' : sec_staff, 'var_1_identification' : var_1_identification,
                   'var_2_encoding': var_2_encoding,'var_2_printing' : var_2_printing,
                   'var_3' : var_3,'var_4':var_4 ,'var_5' : var_5,'var_5_1': var_5_1,'var_6':var_6})

@login_required(login_url='/tat_sys/login')
def edit_process(request):
    batch_id = request.POST['batch_id']
    batch = Batches.objects.get(id=batch_id)
    if request.method == 'POST':
        process = request.POST['process']
        process_id = request.POST['process_id']
        
        start_date = true_value(request.POST.get('start_date'))
        start_sign = true_value(request.POST.get('start_sign',default=None))
        finish_date = true_value(request.POST.get('date_finish',default=None))
        finish_sign = true_value(request.POST.get('finish_sign',default=None))
        remarks = true_value(request.POST.get('remarks',default=None))
        start_date = process_datetime(start_date)
        finish_date = process_datetime(finish_date)
        
        
        
        Process.objects.filter(id=process_id).update(start_date=start_date,
                                                         start_sign=start_sign,finish_date=finish_date,finish_sign=finish_sign,
                                                         days_completed=get_days_completed(start_date,finish_date),running_tat=get_running_tat(batch.date_received,finish_date),
                                                         remarks=remarks)
        
        p = Process.objects.get(id=process_id)
        
        if p.finish_date != None and p.finish_sign != None:
            if process == '1_receiving':
                if check_for_creation('1_identification',p.id):
                    batch.process_set.create(process="1_identification",start_date=finish_date)
            elif process == '1_identification':
                if check_for_creation('2_encoding',p.id):
                    batch.process_set.create(process="2_encoding",start_date=finish_date)
            elif process == '2_encoding':
                if check_for_creation('2_printing',p.id):
                    batch.process_set.create(process="2_printing",start_date=finish_date)
            elif process == '2_printing':
                if check_for_creation_multiple('3_lab_staff',batch_id):
                    batch.process_set.create(process="3_lab_staff",start_date=finish_date)
                    batch.process_set.create(process="3_dmu_staff")
                    batch.process_set.create(process="3_lab_staff")
                    batch.process_set.create(process="3_dmu_staff")
                    batch.process_set.create(process="4_lab_director")
                    batch.process_set.create(process="4_lab_tech")
                    batch.process_set.create(process="5_concordance")
                    batch.process_set.create(process="5_1_MSII")
                    batch.process_set.create(process="5_1_MSIV")
                    batch.process_set.create(process="6_secretariat")
                    batch.process_set.create(process="6_lab_tech")
    
            
            
    return HttpResponseRedirect(batch.get_absolute_url())


@login_required(login_url='/tat_sys/login')
def add_process(request):
    batch_id = request.POST['batch_id']
    batch = Batches.objects.get(id=batch_id)
    if request.method == 'POST':
        process = request.POST['process']
        
        if '3_' in process:
            batch.process_set.create(process="3_lab_staff")
            batch.process_set.create(process="3_dmu_staff")
        elif '4_' in process:
            batch.process_set.create(process="4_lab_director")
            batch.process_set.create(process="4_lab_tech")
        elif '5_concordance' in process:
            batch.process_set.create(process="5_concordance")
        elif '5_1_' in process:
            batch.process_set.create(process="5_1_MSII")
            batch.process_set.create(process="5_1_MSIV")
        elif '6_' in process:
            batch.process_set.create(process="6_secretariat")
            batch.process_set.create(process="6_lab_tech")
        
        
    return HttpResponseRedirect(batch.get_absolute_url())


@login_required(login_url='/tat_sys/login')
def finish_batch(request):
    batch_id = request.POST['batch_id']
    batch = Batches.objects.get(id=batch_id)
    p = Process.objects.filter(batch_id=batch.id).filter(process__startswith='6_lab_tech').last()
    holidays = Holiday.objects.all().values_list('holiday',flat=True)
    diff = np.busday_count( batch.date_received,p.finish_date,holidays=holidays,weekmask=[1,1,1,1,1,1,0])
    
    if int(diff) < 50:
        Batches.objects.filter(id=batch.id).update(status='Completed')
    elif int(diff) > 50:
         Batches.objects.filter(id=batch.id).update(status='Overdue')
        
        
    return HttpResponseRedirect(batch.get_absolute_url())

def get_days_completed(start_date,finish_date):
    if start_date != None and finish_date != None:
        holidays = Holiday.objects.all().values_list('holiday',flat=True)
        diff = np.busday_count(start_date.date(),finish_date.date(),holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
        return diff
    else:
        return None


def get_running_tat(start_date,finish_date):
    if finish_date != None:
        holidays = Holiday.objects.all().values_list('holiday',flat=True)
        diff = np.busday_count(start_date,finish_date.date(),holidays=holidays,weekmask=[1,1,1,1,1,1,0])
        return diff
    else:
        return None
 
def process_datetime(date_process):
    if '/' in date_process:
        date_process = datetime.datetime.strptime(date_process, '%m/%d/%Y')
        
        date_process = datetime.datetime.strftime(date_process, '%Y-%m-%d')

        date_process = datetime.datetime.strptime(date_process, '%Y-%m-%d')
        
        return date_process
    else:
        return None
        

def check_for_creation(process,process_id):
    p = Process.objects.filter(id=process_id).filter(process=process).exists()
    
    if p:
        return False
    else:
        return True
    
    
def check_for_creation_multiple(process,process_id):
    p = Process.objects.filter(batch_id=process_id).filter(process=process).exists()
    
    if p:
        return False
    else:
        return True
    
    
def true_value(var):
    if var == None:
        return None
    else:
        return var
    
    
def get_variable_value(batch_id,process):
     try:
        ret = Process.objects.filter(batch_id=batch_id).filter(process=process).get()
     except Process.DoesNotExist:
        ret = None
        
     return ret
 
 
def get_variable_many_value(batch_id,process):
    try:
        ret = Process.objects.filter(batch_id=batch_id).filter(process__startswith=process).order_by('created_at')
        # list(reversed(PostModel.objects.filter(author = name[0])))
    except Process.DoesNotExist:
        ret = None
    
    return ret
    
    