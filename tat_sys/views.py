from weakref import ref
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import datetime
from datetime import timedelta
from tat_sys.models import Holiday, Referred, SitePatienInformation, SiteIsolteInformation, SitePhenotypicResult, SiteOrganismResult, SiteDiskResult, SiteMicResult, ArsrlDiskResult, ArsrlMicResult, ArsrlOrganismInformation, ArsrlRecommendation, Hospital
from django.db import IntegrityError
import os
import pandas as pd
import numpy as np
from tat_sys.helper.save_referred import create_or_updated_referred, create_or_updated_referred_lab
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weasyprint import HTML
from django.template.loader import get_template
from datetime import datetime
from tat_sys.helper.abx_panels import select_panel

# Create your views here.
dirpath = os.getcwd()

lab_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Lab')
dmu_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Dmu')
sec_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Secretariat')

lab_staff = lab_staff['Staff Name'].values.tolist()
dmu_staff = dmu_staff['Staff Name'].values.tolist()
sec_staff = sec_staff['Staff Name'].values.tolist()

all_org = pd.read_excel(dirpath + '/tat_sys/static/excel_files/org_all.xlsx')
org_code = all_org['ORG'].values.tolist()
org_name = all_org['ORG_CLEAN'].values.tolist()

# @login_required(login_url='/tat_sys/login')
# def qr_code(request):
#     return render(request, 'tat_sys/qr-code.html')


@login_required(login_url='/tat_sys/login')
def generate_report(request,uuid):
    p = Referred.objects.filter(uuid=uuid).first()
    patient_info = SitePatienInformation.objects.filter(referred=p).first()
    isolate_info = SiteIsolteInformation.objects.filter(referred=p).first()
    phenotypic_result = SitePhenotypicResult.objects.filter(referred=p).first()
    organism_result = SiteOrganismResult.objects.filter(referred=p).first()
    site_abx_disk_panel, site_abx_mic_panel = select_panel(organism_result.org_code)
    site_disk = SiteDiskResult.objects.filter(referred=p).first()
    site_mic = SiteMicResult.objects.filter(referred=p).first()
    ars_org_info = ArsrlOrganismInformation.objects.filter(referred=p).first()
    ars_abx_disk_panel, ars_abx_mic_panel = select_panel(ars_org_info.org_code)
    ars_recommendation = ArsrlRecommendation.objects.filter(referred=p).first()
    ars_disk = ArsrlDiskResult.objects.filter(referred=p).first()
    ars_mic = ArsrlMicResult.objects.filter(referred=p).first()
    # Load your template
    template = get_template('template.html')

    # Context data to render the template
    context = {
        'title': p.accession_number + ' - ' + p.hospital_code.hospital_name + '[ ' + datetime.now().strftime('%m_%d_%Y') + ' ]',
        'referred': p,
        'patient_info' : patient_info,
        'isolate_info' : isolate_info,
        'site_organism_result' : organism_result,
        'ars_org_code' : ars_org_info.org_code,
        'site_disk' : [(field_name, getattr(site_disk, field_name)) for field_name in site_abx_disk_panel],
        'site_mic' : [(field_name, getattr(site_mic, field_name)) for field_name in site_abx_mic_panel],
        'ars_disk' : [(field_name, getattr(ars_disk, field_name)) for field_name in ars_abx_disk_panel],
        'ars_mic' : [(field_name, getattr(ars_mic, field_name)) for field_name in ars_abx_mic_panel],
        'ars_organism_result': ars_org_info
    }

    # Render the HTML template with context data
    html = template.render(context)

    # Generate the PDF
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    # Create a response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'

    return response

def update_org_code(request):
        selected_org_code = request.GET.get('org_code', None)
        
        # Assuming the Excel file is named 'hospitals.xlsx' and is located in the same directory as your Django app
        excel_file_path = dirpath + '/tat_sys/static/excel_files/abx_all.xlsx'
        
        try:
            # Read the Excel file
            excel_data = pd.read_excel(excel_file_path, sheet_name='eco')
            
            # Convert the DataFrame to a list of dictionaries
            table_data = excel_data.to_dict(orient='records')
            
            # Return the table data as a JSON response
            return JsonResponse(table_data, safe=False)
        
        
        except Exception as e:
            # Handle exceptions such as FileNotFoundError, SheetNotInDefinedNameError, etc.
            return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/tat_sys/login')
def save_referred(request):

    referred = create_or_updated_referred(request)
    uuid = request.POST['referred_uuid']
    p = Referred.objects.filter(uuid=uuid).first()
    patient_info = SitePatienInformation.objects.filter(referred=p).first()
    isolate_info = SiteIsolteInformation.objects.filter(referred=p).first()
    phenotypic_result = SitePhenotypicResult.objects.filter(referred=p).first()
    organism_result = SiteOrganismResult.objects.filter(referred=p).first()
    site_disk = SiteDiskResult.objects.filter(referred=p).first()
    site_mic = SiteMicResult.objects.filter(referred=p).first()
    ars_org_info = ArsrlOrganismInformation.objects.filter(referred=p).first()
    ars_recommendation = ArsrlRecommendation.objects.filter(referred=p).first()
    ars_disk = ArsrlDiskResult.objects.filter(referred=p).first()
    ars_mic = ArsrlMicResult.objects.filter(referred=p).first()
    return redirect('/tat_sys/referred_view/' + uuid,referred = p, patient_info = patient_info, isolate_info =isolate_info, phenotypic_result = phenotypic_result,
                                                    organism_result = organism_result ,site_disk =site_disk, site_mic = site_mic, ars_org_info = ars_org_info, 
                                                    ars_recommendation = ars_recommendation, ars_disk = ars_disk, ars_mic = ars_mic,org_code = org_code)



@login_required(login_url='/tat_sys/login')
def save_referred_lab(request):
    referred = create_or_updated_referred_lab(request)
    uuid = request.POST['referred_uuid']
    p = Referred.objects.filter(uuid=uuid).first()
    patient_info = SitePatienInformation.objects.filter(referred=p).first()
    isolate_info = SiteIsolteInformation.objects.filter(referred=p).first()
    phenotypic_result = SitePhenotypicResult.objects.filter(referred=p).first()
    organism_result = SiteOrganismResult.objects.filter(referred=p).first()
    site_disk = SiteDiskResult.objects.filter(referred=p).first()
    site_mic = SiteMicResult.objects.filter(referred=p).first()
    ars_org_info = ArsrlOrganismInformation.objects.filter(referred=p).first()
    ars_recommendation = ArsrlRecommendation.objects.filter(referred=p).first()
    ars_disk = ArsrlDiskResult.objects.filter(referred=p).first()
    ars_mic = ArsrlMicResult.objects.filter(referred=p).first()
    return redirect('/tat_sys/referred_view/' + uuid,referred = p, patient_info = patient_info, isolate_info =isolate_info, phenotypic_result = phenotypic_result,
                                                    organism_result = organism_result ,site_disk =site_disk, site_mic = site_mic, ars_org_info = ars_org_info, 
                                                    ars_recommendation = ars_recommendation, ars_disk = ars_disk, ars_mic = ars_mic,org_code = org_code)
  


@login_required(login_url='/tat_sys/login')
def referred_view(request,uuid):
    p = Referred.objects.filter(uuid=uuid).first()
    patient_info = SitePatienInformation.objects.filter(referred=p).first()
    isolate_info = SiteIsolteInformation.objects.filter(referred=p).first()
    phenotypic_result = SitePhenotypicResult.objects.filter(referred=p).first()
    organism_result = SiteOrganismResult.objects.filter(referred=p).first()
    site_disk = SiteDiskResult.objects.filter(referred=p).first()
    site_mic = SiteMicResult.objects.filter(referred=p).first()
    ars_org_info = ArsrlOrganismInformation.objects.filter(referred=p).first()
    ars_recommendation = ArsrlRecommendation.objects.filter(referred=p).first()
    ars_disk = ArsrlDiskResult.objects.filter(referred=p).first()
    ars_mic = ArsrlMicResult.objects.filter(referred=p).first()
    return render(request, 'tat_sys/referred.html',{'referred' : p, 'patient_info' : patient_info, 'isolate_info' : isolate_info, 'phenotypic_result' : phenotypic_result,
                                                    'organism_result' : organism_result ,'site_disk' : site_disk, 'site_mic' : site_mic,
                                                    'ars_org_info' : ars_org_info, 'ars_recommendation' : ars_recommendation, 'ars_disk' : ars_disk, 'ars_mic' : ars_mic, 'all_org' : all_org})





@login_required(login_url='/tat_sys/login')
def referred_list_view(request,uuid):
    p = Referred.objects.all()
    return render(request, 'tat_sys/referred_list.html',{'batches' : p})



@login_required(login_url='/tat_sys/login')
def create_referred(request):
    # batch_id = request.POST['create_batch_id']
    # reference_number = request.POST['reference_number']
    # lab_number = request.POST['lab_number']
    # batch = Batches.objects.filter(id=batch_id).first()
    # user = str(request.user.first_name) + ' ' + str(request.user.last_name)
    # batch.referred_set.create(reference_number=reference_number,lab_number=lab_number,created_by=user)
    hospital_code = request.POST['hospital_code']
    accession_number = request.POST['accession_number']
    user = str(request.user.username)
    # Perform validation
    try:
        referred = Referred(accession_number=accession_number, hospital_code_id=hospital_code,created_by=user)
        referred.full_clean()  # This will trigger model validation
    except ValidationError as e:
        errors = e.message_dict
        return render(request, 'encoding.html', {'errors': errors})
    else:
        # Save the referred object if validation passes
        referred.save()
        # Redirect or render success page
        # return redirect('success_url')
        # or
        # return render(request, 'success.html')
    return HttpResponseRedirect('/tat_sys/encoding')



@login_required(login_url='/tat_sys/login')
def encoding_view(request):
    # batches = Batches.objects.all().order_by('-created_at')
    hospitals = Hospital.objects.all()
    referreds = Referred.objects.all().order_by('-created_at')
    if request.user.groups.filter(name='SiteEncoder').exists():
        referreds = Referred.objects.filter(hospital_code=request.user.userprofile.hospital).order_by('-created_at')

    return render(request, 'tat_sys/encoding.html',{'lab_staff':lab_staff,'dmu_staff':dmu_staff,'sec_staff':sec_staff,'hospitals':hospitals, 'referreds':referreds})
    # return render(request, 'tat_sys/encoding.html',{'batches': batches,'lab_staff':lab_staff,'dmu_staff':dmu_staff,'sec_staff':sec_staff})


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

    return HttpResponseRedirect('/tat_sys/encoding')


@login_required(login_url='/tat_sys/login')
def delete_package(request):
    package_id = request.POST['package_id']
    Packages.objects.filter(id=package_id).delete()

    return HttpResponseRedirect('/tat_sys/receiving')


# GET : view for landing page
@login_required(login_url='/tat_sys/login')
def tat_landing(request):
#     on_going_tat = Batches.objects.filter(status=None).count()
# # on_going_tat = Batches.dashboard.count()
#     warning_tat = Batches.objects.filter(date_received__lt=datetime.datetime.now() - timedelta(days=40)).filter(date_received__gt=datetime.datetime.now() - timedelta(days=50)).count()
#     overdue_tat = Batches.objects.filter(status='Overdue').count()
#     ontime_tat = Batches.objects.filter(status='Completed').count()
#     batches = Batches.objects.filter(status=None)
    
    on_going_tat = 0
# on_going_tat = Batches.dashboard.count()
    warning_tat = 0
    overdue_tat = 0
    ontime_tat = 0
    batches = 0
    
    
    processing = 0
    encoding = 0
    editing = 0
    lab_verify = 0
    final_verify = 0
    releasing = 0
    
    
    # for batch in batches:
    #     if 'Processing' in batch.get_current_status:
    #         processing += 1
    #     elif 'Encoding' in batch.get_current_status:
    #         encoding += 1
    #     elif 'Editing' in batch.get_current_status:
    #         editing += 1
    #     elif 'Lab Verification' in batch.get_current_status:
    #         lab_verify += 1
    #     elif 'Final Verification' in batch.get_current_status:
    #         final_verify += 1  
    #     elif 'Releasing' in batch.get_current_status:
    #         releasing += 1
    

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
        batch_number = request.POST['batch_number']
        total_batch_number = request.POST['total_batch_number']
        date_received = request.POST['date_received']
        datereceived =  datetime.datetime.strptime(date_received, '%m/%d/%Y')
        
        date_received = date_received.replace('/','')
        start = date_received[:4]
        end = date_received[-2:]
        date_received = start + end
        
        received_by = request.POST['received_by']
        
        accession_number = accession_number.replace(" ","")
        
        batch_name = site + '_' + date_received + '_' + str(batch_number) + '.' + str(total_batch_number) + '_' + accession_number
        
        try:
            batch = Batches.objects.create(batch_name=batch_name,
                                site=site,
                                accession_number=accession_number,
                                batch_number=batch_number,
                                total_batch_number=total_batch_number,
                                date_received=datereceived,
                                received_by=received_by)
            batch.process_set.create(process="1_receiving",start_date=batch.date_received)
            return HttpResponseRedirect('/tat_sys/encoding')
        except:
            return HttpResponseRedirect('/tat_sys/encoding')
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
def qr_code(request,batch_uuid):
    p = Batches.objects.get(uuid=batch_uuid)
    current_holder = p.get_current_holder
    return render(request, 'tat_sys/qr-code.html',{'current_holder' : current_holder,'batch' : p})


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
                if not check_for_creation('1_identification',p.id):
                    batch.process_set.create(process="1_identification",start_date=finish_date)
            elif process == '1_identification':
                if not check_for_creation('2_encoding',p.id):
                    batch.process_set.create(process="2_encoding",start_date=finish_date)
            elif process == '2_encoding':
                if not check_for_creation('2_printing',p.id):
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
    
    return p
    
    # if p:
    #     return True
    # else:
    #     return False
    
    
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
    
    