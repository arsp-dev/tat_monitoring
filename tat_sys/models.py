from django.db import models
import pandas as pd
import numpy as np
import datetime
from django.forms import model_to_dict
import uuid
import os
from django.contrib.auth import get_user_model


dirpath = os.getcwd()

lab_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Lab')
dmu_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Dmu')
sec_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Secretariat')

lab_staff = lab_staff['Staff Name'].values.tolist()
dmu_staff = dmu_staff['Staff Name'].values.tolist()
sec_staff = sec_staff['Staff Name'].values.tolist()
# Create your models here.


class Packages(models.Model):
    package_name = models.TextField(null=True,blank=True,default=None,unique=True)
    site = models.TextField(max_length=3)
    date_received = models.DateField()
    received_by = models.TextField(max_length=99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.package_name
    
    def get_number_of_batches(self):
        count = Batches.objects.filter(batch_name__startswith=self.package_name).count()
        
        return count
        

class Batches(models.Model):
    batch_name = models.TextField(null=True,blank=True,default=None,unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    site = models.TextField(max_length=3)
    accession_number = models.TextField(max_length=99)
    batch_number = models.IntegerField()
    total_batch_number = models.IntegerField()
    date_received = models.DateField()
    received_by = models.TextField(max_length=99)
    status = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def get_reference_number(self):
        s = self.accession_number
        s = s.replace(" ","")
        n = s.split("-")
        count = Referred.objects.filter(batch=self.id).count()
        return int(n[0]) + count
    
    
    @property
    def get_lab_number(self):
        s = self.accession_number
        s = s.replace(" ","")
        n = s.split("-")
        count = Referred.objects.filter(batch=self.id).count()
        trailing_txt = "{:04d}".format(int(n[0]) + count)
        year = datetime.date.today().strftime("%y")
        return str(year) + 'ARS_' + str(self.site) + str(trailing_txt) 
    
    
    @property
    def number_of_isolate_encoded(self):
        return Referred.objects.filter(batch=self.id).count()
        
    
    
    @property
    def number_of_isolates(self):
        s = self.accession_number
        s = s.replace(" ","")
        n = s.split("-")
        
        return (int(n[1]) - int(n[0])) + 1
    
    
    @property
    def get_current_status(self):
        p = Process.objects.filter(batch_id=self.id).last()
        ret = p.process
        suff = ''
        if p.finish_sign != None:
            if p.finish_sign in lab_staff:
                suff = 'Lab'
            elif p.finish_sign in sec_staff or p.finish_sign in dmu_staff:
                suff = 'Office'
            
            
        else:
            if p.start_sign in lab_staff:
                suff = 'Lab'
            elif p.start_sign in sec_staff or p.start_sign in dmu_staff:
                suff = 'Office'
           
        
        
        if '1_' in ret:
            if suff != '':
                ret = 'Processing' + ' (' + suff + ')'
            else:
                ret = 'Processing'
        elif '2_' in ret:
            if suff != '':
                ret = 'Encoding' + ' (' + suff + ')'
            else:
                ret = 'Encoding'
        elif '3_' in ret:
            if suff != '':
                ret = 'Editing' + ' (' + suff + ')'
            else:
                ret = 'Editing'
        elif '4_' in ret:
            if suff != '':
                ret = 'Lab Verification' + ' (' + suff + ')'
            else:
                ret = 'Lab Verification'
        elif '5_' in ret:
            if suff != '':
                ret = 'Final Verification' + ' (' + suff + ')'
            else:
                ret = 'Final Verification'
        elif '6_' in ret:
            if suff != '':
                ret = 'Releasing' + ' (' + suff + ')'
            else:
                ret = 'Releasing'
            
        return ret
   
   
    @property
    def get_running_tat(self):
        holidays = Holiday.objects.all().values_list('holiday',flat=True)
        diff = np.busday_count( self.date_received,datetime.date.today(),holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
        return diff
    
    
  

    def __str__(self):
        return self.batch_name
    
    
    
    
    def get_absolute_url(self):
        return "batches/%i/" % self.id
    
    @property
    def get_encoding_url(self):
        return "encoding/" + str(self.uuid) + '/'
    
    @property
    def get_qr_code_url(self):
        return "http://10.10.25.178:8081/tat_sys/qr-code/" + str(self.uuid) + '/'
    
    
    @property
    def get_current_holder(self):
        p = Process.objects.filter(batch_id=self.id).last()
        suff = ''
        if p.finish_sign != None:
           suff = p.finish_sign  
        else:
            suff = p.start_sign
        
        return suff
    
    
    
    def get_format_date(self):
        date_received = datetime.datetime.strftime(self.date_received, '%m/%d/%Y')
        return date_received
    
    def get_days_completed(self):
        p = Process.objects.filter(batch_id=self.id)
        p = p.exclude(days_completed=None)
        p = p.values_list('days_completed', flat=True)
        p = [int(i) for i in p] 
        days_completed = sum(p)
        
        return days_completed
    
    def get_final_running_tat(self):
        p = Process.objects.filter(batch_id=self.id).filter(process__startswith='6_lab_tech').last()
        diff = '---'
        if p != None:
            if p.finish_date != None:
                batch = Batches.objects.get(id=self.id)
                holidays = Holiday.objects.all().values_list('holiday',flat=True)
                diff = np.busday_count( batch.date_received,p.finish_date,holidays=holidays,weekmask=[1,1,1,1,1,1,0])
          
               
        return diff

  
        
        
        
        

class Holiday(models.Model):
    holiday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.holiday
    
    def get_new_format(self):
        holiday = datetime.datetime.strftime(self.holiday, '%Y-%m-%d')
        return holiday
    
    
    def get_new_format_post(self):
        holiday = datetime.datetime.strftime(self.holiday, '%m/%d/%Y')
        return holiday


class Referred(models.Model):
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    reference_number = models.TextField(null=True,blank=True,default=None)
    lab_number = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    
    def __str__(self):
        return self.lab_number
    
    
    @property
    def get_referred_url(self):
        return "referred_view/" + str(self.uuid) + '/'


class SitePatienInformation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    patient_number = models.TextField(null=True,default=None)
    date_of_birth = models.DateField(null=True, blank=True,default=None)
    first_name = models.TextField(null=True,blank=True,default=None)
    middle_name = models.TextField(null=True,blank=True,default=None)
    last_name = models.TextField(null=True,blank=True,default=None)
    sex = models.TextField(null=True,blank=True,default=None)
    date_of_admission = models.DateField(null=True, blank=True,default=None)
    nosocomial = models.TextField(null=True,blank=True,default=None)
    diagnosis = models.TextField(null=True,blank=True,default=None)
    icd_10_code = models.TextField(null=True,blank=True,default=None)
    ward = models.TextField(null=True,blank=True,default=None)
    service_type = models.TextField(null=True,blank=True,default=None)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    

class SiteIsolteInformation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    specimen_number = models.TextField(null=True,blank=True,default=None)
    specimen_date = models.DateField(null=True, blank=True,default=None)
    specimen_type = models.TextField(null=True,blank=True,default=None)
    reason_for_referral = models.TextField(null=True,blank=True,default=None)
    growth = models.TextField(null=True,blank=True,default=None)
    urine_count = models.TextField(null=True,blank=True,default=None)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.specimen_number
    
    


class SitePhenotypicResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    ampc = models.TextField(null=True,blank=True,default=None)
    esbl = models.TextField(null=True,blank=True,default=None)
    carb = models.TextField(null=True,blank=True,default=None)
    mbl = models.TextField(null=True,blank=True,default=None)
    bl = models.TextField(null=True,blank=True,default=None)
    mr = models.TextField(null=True,blank=True,default=None)
    meca = models.TextField(null=True,blank=True,default=None)
    icr = models.TextField(null=True,blank=True,default=None)
    others = models.TextField(null=True,blank=True,default=None)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred
    
    
    
class SiteOrganismResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    site_pre = models.TextField(null=True,blank=True,default=None)
    org_code = models.TextField(null=True,blank=True,default=None)
    org_site = models.TextField(null=True,blank=True,default=None)
    site_post = models.TextField(null=True,blank=True,default=None)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred


class SiteDiskResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amk_disk = models.TextField(null=True,blank=True,default=None)
    amk_disk_ris = models.TextField(null=True,blank=True,default=None)
    amc_disk = models.TextField(null=True,blank=True,default=None)
    amc_disk_ris = models.TextField(null=True,blank=True,default=None)
    amp_disk = models.TextField(null=True,blank=True,default=None)
    amp_disk_ris = models.TextField(null=True,blank=True,default=None)
    sam_disk = models.TextField(null=True,blank=True,default=None)
    sam_disk_ris = models.TextField(null=True,blank=True,default=None)
    atm_disk = models.TextField(null=True,blank=True,default=None)
    atm_disk_ris = models.TextField(null=True,blank=True,default=None)
    azm_disk = models.TextField(null=True,blank=True,default=None)
    azm_disk_ris = models.TextField(null=True,blank=True,default=None)
    cec_disk = models.TextField(null=True,blank=True,default=None)
    cec_disk_ris = models.TextField(null=True,blank=True,default=None)
    man_disk = models.TextField(null=True,blank=True,default=None)
    man_disk_ris = models.TextField(null=True,blank=True,default=None)
    czo_disk = models.TextField(null=True,blank=True,default=None)
    czo_disk_ris = models.TextField(null=True,blank=True,default=None)
    fep_disk = models.TextField(null=True,blank=True,default=None)
    fep_disk_ris = models.TextField(null=True,blank=True,default=None)
    cfm_disk = models.TextField(null=True,blank=True,default=None)
    cfm_disk_ris = models.TextField(null=True,blank=True,default=None)
    cfp_disk = models.TextField(null=True,blank=True,default=None)
    cfp_disk_ris = models.TextField(null=True,blank=True,default=None)
    ctx_disk = models.TextField(null=True,blank=True,default=None)
    ctx_disk_ris = models.TextField(null=True,blank=True,default=None)
    fox_disk = models.TextField(null=True,blank=True,default=None)
    fox_disk_ris = models.TextField(null=True,blank=True,default=None)
    caz_disk = models.TextField(null=True,blank=True,default=None)
    caz_disk_ris = models.TextField(null=True,blank=True,default=None)
    cro_disk = models.TextField(null=True,blank=True,default=None)
    cro_disk_ris = models.TextField(null=True,blank=True,default=None)
    cxa_disk = models.TextField(null=True,blank=True,default=None)
    cxa_disk_ris = models.TextField(null=True,blank=True,default=None)
    cep_disk = models.TextField(null=True,blank=True,default=None)
    cep_disk_ris = models.TextField(null=True,blank=True,default=None)
    chl_disk = models.TextField(null=True,blank=True,default=None)
    chl_disk_ris = models.TextField(null=True,blank=True,default=None)
    cip_disk = models.TextField(null=True,blank=True,default=None)
    cip_disk_ris = models.TextField(null=True,blank=True,default=None)
    clr_disk = models.TextField(null=True,blank=True,default=None)
    clr_disk_ris = models.TextField(null=True,blank=True,default=None)
    cli_disk = models.TextField(null=True,blank=True,default=None)
    cli_disk_ris = models.TextField(null=True,blank=True,default=None)
    sxt_disk = models.TextField(null=True,blank=True,default=None)
    sxt_disk_ris = models.TextField(null=True,blank=True,default=None)
    ery_disk = models.TextField(null=True,blank=True,default=None)
    ery_disk_ris = models.TextField(null=True,blank=True,default=None)
    gen_disk = models.TextField(null=True,blank=True,default=None)
    gen_disk_ris = models.TextField(null=True,blank=True,default=None)
    ipm_disk = models.TextField(null=True,blank=True,default=None)
    ipm_disk_ris = models.TextField(null=True,blank=True,default=None)
    kan_disk = models.TextField(null=True,blank=True,default=None)
    kan_disk_ris = models.TextField(null=True,blank=True,default=None)
    lev_disk = models.TextField(null=True,blank=True,default=None)
    lev_disk_ris = models.TextField(null=True,blank=True,default=None)
    nal_disk = models.TextField(null=True,blank=True,default=None)
    nal_disk_ris = models.TextField(null=True,blank=True,default=None)
    net_disk = models.TextField(null=True,blank=True,default=None)
    net_disk_ris = models.TextField(null=True,blank=True,default=None)
    nit_disk = models.TextField(null=True,blank=True,default=None)
    nit_disk_ris = models.TextField(null=True,blank=True,default=None)
    nor_disk = models.TextField(null=True,blank=True,default=None)
    nor_disk_ris = models.TextField(null=True,blank=True,default=None)
    ofx_disk = models.TextField(null=True,blank=True,default=None)
    ofx_disk_ris = models.TextField(null=True,blank=True,default=None)
    oxa_disk = models.TextField(null=True,blank=True,default=None)
    oxa_disk_ris = models.TextField(null=True,blank=True,default=None)
    pen_disk = models.TextField(null=True,blank=True,default=None)
    pen_disk_ris = models.TextField(null=True,blank=True,default=None)
    pip_disk = models.TextField(null=True,blank=True,default=None)
    pip_disk_ris = models.TextField(null=True,blank=True,default=None)
    rif_disk = models.TextField(null=True,blank=True,default=None)
    rif_disk_ris = models.TextField(null=True,blank=True,default=None)
    spe_disk = models.TextField(null=True,blank=True,default=None)
    spe_disk_ris = models.TextField(null=True,blank=True,default=None)
    str_disk = models.TextField(null=True,blank=True,default=None)
    str_disk_ris = models.TextField(null=True,blank=True,default=None)
    tet_disk = models.TextField(null=True,blank=True,default=None)
    tet_disk_ris = models.TextField(null=True,blank=True,default=None)
    tic_disk = models.TextField(null=True,blank=True,default=None)
    tic_disk_ris = models.TextField(null=True,blank=True,default=None)
    tcc_disk = models.TextField(null=True,blank=True,default=None)
    tcc_disk_ris = models.TextField(null=True,blank=True,default=None)
    tob_disk = models.TextField(null=True,blank=True,default=None)
    tob_disk_ris = models.TextField(null=True,blank=True,default=None)
    van_disk = models.TextField(null=True,blank=True,default=None)
    van_disk_ris = models.TextField(null=True,blank=True,default=None)
    mfx_disk = models.TextField(null=True,blank=True,default=None)
    mfx_disk_ris = models.TextField(null=True,blank=True,default=None)
    mem_disk = models.TextField(null=True,blank=True,default=None)
    mem_disk_ris = models.TextField(null=True,blank=True,default=None)
    tzp_disk = models.TextField(null=True,blank=True,default=None)
    tzp_disk_ris = models.TextField(null=True,blank=True,default=None)
    geh_disk = models.TextField(null=True,blank=True,default=None)
    geh_disk_ris = models.TextField(null=True,blank=True,default=None)
    sth_disk = models.TextField(null=True,blank=True,default=None)
    sth_disk_ris = models.TextField(null=True,blank=True,default=None)
    lnz_disk = models.TextField(null=True,blank=True,default=None)
    lnz_disk_ris = models.TextField(null=True,blank=True,default=None)
    nov_disk = models.TextField(null=True,blank=True,default=None)
    nov_disk_ris = models.TextField(null=True,blank=True,default=None)
    etp_disk = models.TextField(null=True,blank=True,default=None)
    etp_disk_ris = models.TextField(null=True,blank=True,default=None)
    dor_disk = models.TextField(null=True,blank=True,default=None)
    dor_disk_ris = models.TextField(null=True,blank=True,default=None)
    tgc_disk = models.TextField(null=True,blank=True,default=None)
    tgc_disk_ris = models.TextField(null=True,blank=True,default=None)
    col_disk = models.TextField(null=True,blank=True,default=None)
    col_disk_ris = models.TextField(null=True,blank=True,default=None)
    pol_disk = models.TextField(null=True,blank=True,default=None)
    pol_disk_ris = models.TextField(null=True,blank=True,default=None)
    dox_disk = models.TextField(null=True,blank=True,default=None)
    dox_disk_ris = models.TextField(null=True,blank=True,default=None)
    qda_disk = models.TextField(null=True,blank=True,default=None)
    qda_disk_ris = models.TextField(null=True,blank=True,default=None)
    mno_disk = models.TextField(null=True,blank=True,default=None)
    mno_disk_ris = models.TextField(null=True,blank=True,default=None)
    dap_disk = models.TextField(null=True,blank=True,default=None)
    dap_disk_ris = models.TextField(null=True,blank=True,default=None)
    comments = models.TextField(null=True,blank=True,default=None)
    
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred
    
    

class SiteMicResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amk_mic = models.TextField(null=True,blank=True,default=None)
    amk_mic_ris = models.TextField(null=True,blank=True,default=None)
    amc_mic = models.TextField(null=True,blank=True,default=None)
    amc_mic_ris = models.TextField(null=True,blank=True,default=None)
    amp_mic = models.TextField(null=True,blank=True,default=None)
    amp_mic_ris = models.TextField(null=True,blank=True,default=None)
    sam_mic = models.TextField(null=True,blank=True,default=None)
    sam_mic_ris = models.TextField(null=True,blank=True,default=None)
    atm_mic = models.TextField(null=True,blank=True,default=None)
    atm_mic_ris = models.TextField(null=True,blank=True,default=None)
    azm_mic = models.TextField(null=True,blank=True,default=None)
    azm_mic_ris = models.TextField(null=True,blank=True,default=None)
    cec_mic = models.TextField(null=True,blank=True,default=None)
    cec_mic_ris = models.TextField(null=True,blank=True,default=None)
    man_mic = models.TextField(null=True,blank=True,default=None)
    man_mic_ris = models.TextField(null=True,blank=True,default=None)
    czo_mic = models.TextField(null=True,blank=True,default=None)
    czo_mic_ris = models.TextField(null=True,blank=True,default=None)
    fep_mic = models.TextField(null=True,blank=True,default=None)
    fep_mic_ris = models.TextField(null=True,blank=True,default=None)
    cfm_mic = models.TextField(null=True,blank=True,default=None)
    cfm_mic_ris = models.TextField(null=True,blank=True,default=None)
    cfp_mic = models.TextField(null=True,blank=True,default=None)
    cfp_mic_ris = models.TextField(null=True,blank=True,default=None)
    ctx_mic = models.TextField(null=True,blank=True,default=None)
    ctx_mic_ris = models.TextField(null=True,blank=True,default=None)
    fox_mic = models.TextField(null=True,blank=True,default=None)
    fox_mic_ris = models.TextField(null=True,blank=True,default=None)
    caz_mic = models.TextField(null=True,blank=True,default=None)
    caz_mic_ris = models.TextField(null=True,blank=True,default=None)
    cro_mic = models.TextField(null=True,blank=True,default=None)
    cro_mic_ris = models.TextField(null=True,blank=True,default=None)
    cxa_mic = models.TextField(null=True,blank=True,default=None)
    cxa_mic_ris = models.TextField(null=True,blank=True,default=None)
    cep_mic = models.TextField(null=True,blank=True,default=None)
    cep_mic_ris = models.TextField(null=True,blank=True,default=None)
    chl_mic = models.TextField(null=True,blank=True,default=None)
    chl_mic_ris = models.TextField(null=True,blank=True,default=None)
    cip_mic = models.TextField(null=True,blank=True,default=None)
    cip_mic_ris = models.TextField(null=True,blank=True,default=None)
    clr_mic = models.TextField(null=True,blank=True,default=None)
    clr_mic_ris = models.TextField(null=True,blank=True,default=None)
    cli_mic = models.TextField(null=True,blank=True,default=None)
    cli_mic_ris = models.TextField(null=True,blank=True,default=None)
    sxt_mic = models.TextField(null=True,blank=True,default=None)
    sxt_mic_ris = models.TextField(null=True,blank=True,default=None)
    ery_mic = models.TextField(null=True,blank=True,default=None)
    ery_mic_ris = models.TextField(null=True,blank=True,default=None)
    gen_mic = models.TextField(null=True,blank=True,default=None)
    gen_mic_ris = models.TextField(null=True,blank=True,default=None)
    ipm_mic = models.TextField(null=True,blank=True,default=None)
    ipm_mic_ris = models.TextField(null=True,blank=True,default=None)
    kan_mic = models.TextField(null=True,blank=True,default=None)
    kan_mic_ris = models.TextField(null=True,blank=True,default=None)
    lev_mic = models.TextField(null=True,blank=True,default=None)
    lev_mic_ris = models.TextField(null=True,blank=True,default=None)
    nal_mic = models.TextField(null=True,blank=True,default=None)
    nal_mic_ris = models.TextField(null=True,blank=True,default=None)
    net_mic = models.TextField(null=True,blank=True,default=None)
    net_mic_ris = models.TextField(null=True,blank=True,default=None)
    nit_mic = models.TextField(null=True,blank=True,default=None)
    nit_mic_ris = models.TextField(null=True,blank=True,default=None)
    nor_mic = models.TextField(null=True,blank=True,default=None)
    nor_mic_ris = models.TextField(null=True,blank=True,default=None)
    ofx_mic = models.TextField(null=True,blank=True,default=None)
    ofx_mic_ris = models.TextField(null=True,blank=True,default=None)
    oxa_mic = models.TextField(null=True,blank=True,default=None)
    oxa_mic_ris = models.TextField(null=True,blank=True,default=None)
    pen_mic = models.TextField(null=True,blank=True,default=None)
    pen_mic_ris = models.TextField(null=True,blank=True,default=None)
    pip_mic = models.TextField(null=True,blank=True,default=None)
    pip_mic_ris = models.TextField(null=True,blank=True,default=None)
    rif_mic = models.TextField(null=True,blank=True,default=None)
    rif_mic_ris = models.TextField(null=True,blank=True,default=None)
    spe_mic = models.TextField(null=True,blank=True,default=None)
    spe_mic_ris = models.TextField(null=True,blank=True,default=None)
    str_mic = models.TextField(null=True,blank=True,default=None)
    str_mic_ris = models.TextField(null=True,blank=True,default=None)
    tet_mic = models.TextField(null=True,blank=True,default=None)
    tet_mic_ris = models.TextField(null=True,blank=True,default=None)
    tic_mic = models.TextField(null=True,blank=True,default=None)
    tic_mic_ris = models.TextField(null=True,blank=True,default=None)
    tcc_mic = models.TextField(null=True,blank=True,default=None)
    tcc_mic_ris = models.TextField(null=True,blank=True,default=None)
    tob_mic = models.TextField(null=True,blank=True,default=None)
    tob_mic_ris = models.TextField(null=True,blank=True,default=None)
    van_mic = models.TextField(null=True,blank=True,default=None)
    van_mic_ris = models.TextField(null=True,blank=True,default=None)
    mfx_mic = models.TextField(null=True,blank=True,default=None)
    mfx_mic_ris = models.TextField(null=True,blank=True,default=None)
    mem_mic = models.TextField(null=True,blank=True,default=None)
    mem_mic_ris = models.TextField(null=True,blank=True,default=None)
    tzp_mic = models.TextField(null=True,blank=True,default=None)
    tzp_mic_ris = models.TextField(null=True,blank=True,default=None)
    geh_mic = models.TextField(null=True,blank=True,default=None)
    geh_mic_ris = models.TextField(null=True,blank=True,default=None)
    sth_mic = models.TextField(null=True,blank=True,default=None)
    sth_mic_ris = models.TextField(null=True,blank=True,default=None)
    lnz_mic = models.TextField(null=True,blank=True,default=None)
    lnz_mic_ris = models.TextField(null=True,blank=True,default=None)
    nov_mic = models.TextField(null=True,blank=True,default=None)
    nov_mic_ris = models.TextField(null=True,blank=True,default=None)
    etp_mic = models.TextField(null=True,blank=True,default=None)
    etp_mic_ris = models.TextField(null=True,blank=True,default=None)
    dor_mic = models.TextField(null=True,blank=True,default=None)
    dor_mic_ris = models.TextField(null=True,blank=True,default=None)
    tgc_mic = models.TextField(null=True,blank=True,default=None)
    tgc_mic_ris = models.TextField(null=True,blank=True,default=None)
    col_mic = models.TextField(null=True,blank=True,default=None)
    col_mic_ris = models.TextField(null=True,blank=True,default=None)
    pol_mic = models.TextField(null=True,blank=True,default=None)
    pol_mic_ris = models.TextField(null=True,blank=True,default=None)
    dox_mic = models.TextField(null=True,blank=True,default=None)
    dox_mic_ris = models.TextField(null=True,blank=True,default=None)
    qda_mic = models.TextField(null=True,blank=True,default=None)
    qda_mic_ris = models.TextField(null=True,blank=True,default=None)
    mno_mic = models.TextField(null=True,blank=True,default=None)
    mno_mic_ris = models.TextField(null=True,blank=True,default=None)
    dap_mic = models.TextField(null=True,blank=True,default=None)
    dap_mic_ris = models.TextField(null=True,blank=True,default=None)
    
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred
    
    
class ArsrlOrganismInformation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    ampc = models.TextField(null=True,blank=True,default=None)
    esbl = models.TextField(null=True,blank=True,default=None)
    carb = models.TextField(null=True,blank=True,default=None)
    ecim = models.TextField(null=True,blank=True,default=None)
    mcim = models.TextField(null=True,blank=True,default=None)
    ec_mcim = models.TextField(null=True,blank=True,default=None)
    mbl = models.TextField(null=True,blank=True,default=None)
    bl = models.TextField(null=True,blank=True,default=None)
    mr = models.TextField(null=True,blank=True,default=None)
    meca = models.TextField(null=True,blank=True,default=None)
    icr = models.TextField(null=True,blank=True,default=None)
    arsl_pre = models.TextField(null=True,blank=True,default=None)
    org_code = models.TextField(null=True,blank=True,default=None)
    org_name = models.TextField(null=True,blank=True,default=None)
    arsrl_post = models.TextField(null=True,blank=True,default=None)
    
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ArsrlRecommendation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    recommendation_code = models.TextField(null=True,blank=True,default=None)
    recommendation = models.TextField(null=True,blank=True,default=None)
    description = models.TextField(null=True,blank=True,default=None)

    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class ArsrlDiskResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amk_disk = models.TextField(null=True,blank=True,default=None)
    amk_disk_ris = models.TextField(null=True,blank=True,default=None)
    amc_disk = models.TextField(null=True,blank=True,default=None)
    amc_disk_ris = models.TextField(null=True,blank=True,default=None)
    amp_disk = models.TextField(null=True,blank=True,default=None)
    amp_disk_ris = models.TextField(null=True,blank=True,default=None)
    sam_disk = models.TextField(null=True,blank=True,default=None)
    sam_disk_ris = models.TextField(null=True,blank=True,default=None)
    atm_disk = models.TextField(null=True,blank=True,default=None)
    atm_disk_ris = models.TextField(null=True,blank=True,default=None)
    azm_disk = models.TextField(null=True,blank=True,default=None)
    azm_disk_ris = models.TextField(null=True,blank=True,default=None)
    cec_disk = models.TextField(null=True,blank=True,default=None)
    cec_disk_ris = models.TextField(null=True,blank=True,default=None)
    man_disk = models.TextField(null=True,blank=True,default=None)
    man_disk_ris = models.TextField(null=True,blank=True,default=None)
    czo_disk = models.TextField(null=True,blank=True,default=None)
    czo_disk_ris = models.TextField(null=True,blank=True,default=None)
    fep_disk = models.TextField(null=True,blank=True,default=None)
    fep_disk_ris = models.TextField(null=True,blank=True,default=None)
    cfm_disk = models.TextField(null=True,blank=True,default=None)
    cfm_disk_ris = models.TextField(null=True,blank=True,default=None)
    cfp_disk = models.TextField(null=True,blank=True,default=None)
    cfp_disk_ris = models.TextField(null=True,blank=True,default=None)
    ctx_disk = models.TextField(null=True,blank=True,default=None)
    ctx_disk_ris = models.TextField(null=True,blank=True,default=None)
    fox_disk = models.TextField(null=True,blank=True,default=None)
    fox_disk_ris = models.TextField(null=True,blank=True,default=None)
    caz_disk = models.TextField(null=True,blank=True,default=None)
    caz_disk_ris = models.TextField(null=True,blank=True,default=None)
    cro_disk = models.TextField(null=True,blank=True,default=None)
    cro_disk_ris = models.TextField(null=True,blank=True,default=None)
    cxa_disk = models.TextField(null=True,blank=True,default=None)
    cxa_disk_ris = models.TextField(null=True,blank=True,default=None)
    cep_disk = models.TextField(null=True,blank=True,default=None)
    cep_disk_ris = models.TextField(null=True,blank=True,default=None)
    chl_disk = models.TextField(null=True,blank=True,default=None)
    chl_disk_ris = models.TextField(null=True,blank=True,default=None)
    cip_disk = models.TextField(null=True,blank=True,default=None)
    cip_disk_ris = models.TextField(null=True,blank=True,default=None)
    clr_disk = models.TextField(null=True,blank=True,default=None)
    clr_disk_ris = models.TextField(null=True,blank=True,default=None)
    cli_disk = models.TextField(null=True,blank=True,default=None)
    cli_disk_ris = models.TextField(null=True,blank=True,default=None)
    sxt_disk = models.TextField(null=True,blank=True,default=None)
    sxt_disk_ris = models.TextField(null=True,blank=True,default=None)
    ery_disk = models.TextField(null=True,blank=True,default=None)
    ery_disk_ris = models.TextField(null=True,blank=True,default=None)
    gen_disk = models.TextField(null=True,blank=True,default=None)
    gen_disk_ris = models.TextField(null=True,blank=True,default=None)
    ipm_disk = models.TextField(null=True,blank=True,default=None)
    ipm_disk_ris = models.TextField(null=True,blank=True,default=None)
    kan_disk = models.TextField(null=True,blank=True,default=None)
    kan_disk_ris = models.TextField(null=True,blank=True,default=None)
    lev_disk = models.TextField(null=True,blank=True,default=None)
    lev_disk_ris = models.TextField(null=True,blank=True,default=None)
    nal_disk = models.TextField(null=True,blank=True,default=None)
    nal_disk_ris = models.TextField(null=True,blank=True,default=None)
    net_disk = models.TextField(null=True,blank=True,default=None)
    net_disk_ris = models.TextField(null=True,blank=True,default=None)
    nit_disk = models.TextField(null=True,blank=True,default=None)
    nit_disk_ris = models.TextField(null=True,blank=True,default=None)
    nor_disk = models.TextField(null=True,blank=True,default=None)
    nor_disk_ris = models.TextField(null=True,blank=True,default=None)
    ofx_disk = models.TextField(null=True,blank=True,default=None)
    ofx_disk_ris = models.TextField(null=True,blank=True,default=None)
    oxa_disk = models.TextField(null=True,blank=True,default=None)
    oxa_disk_ris = models.TextField(null=True,blank=True,default=None)
    pen_disk = models.TextField(null=True,blank=True,default=None)
    pen_disk_ris = models.TextField(null=True,blank=True,default=None)
    pip_disk = models.TextField(null=True,blank=True,default=None)
    pip_disk_ris = models.TextField(null=True,blank=True,default=None)
    rif_disk = models.TextField(null=True,blank=True,default=None)
    rif_disk_ris = models.TextField(null=True,blank=True,default=None)
    spe_disk = models.TextField(null=True,blank=True,default=None)
    spe_disk_ris = models.TextField(null=True,blank=True,default=None)
    str_disk = models.TextField(null=True,blank=True,default=None)
    str_disk_ris = models.TextField(null=True,blank=True,default=None)
    tet_disk = models.TextField(null=True,blank=True,default=None)
    tet_disk_ris = models.TextField(null=True,blank=True,default=None)
    tic_disk = models.TextField(null=True,blank=True,default=None)
    tic_disk_ris = models.TextField(null=True,blank=True,default=None)
    tcc_disk = models.TextField(null=True,blank=True,default=None)
    tcc_disk_ris = models.TextField(null=True,blank=True,default=None)
    tob_disk = models.TextField(null=True,blank=True,default=None)
    tob_disk_ris = models.TextField(null=True,blank=True,default=None)
    van_disk = models.TextField(null=True,blank=True,default=None)
    van_disk_ris = models.TextField(null=True,blank=True,default=None)
    mfx_disk = models.TextField(null=True,blank=True,default=None)
    mfx_disk_ris = models.TextField(null=True,blank=True,default=None)
    mem_disk = models.TextField(null=True,blank=True,default=None)
    mem_disk_ris = models.TextField(null=True,blank=True,default=None)
    tzp_disk = models.TextField(null=True,blank=True,default=None)
    tzp_disk_ris = models.TextField(null=True,blank=True,default=None)
    geh_disk = models.TextField(null=True,blank=True,default=None)
    geh_disk_ris = models.TextField(null=True,blank=True,default=None)
    sth_disk = models.TextField(null=True,blank=True,default=None)
    sth_disk_ris = models.TextField(null=True,blank=True,default=None)
    lnz_disk = models.TextField(null=True,blank=True,default=None)
    lnz_disk_ris = models.TextField(null=True,blank=True,default=None)
    nov_disk = models.TextField(null=True,blank=True,default=None)
    nov_disk_ris = models.TextField(null=True,blank=True,default=None)
    etp_disk = models.TextField(null=True,blank=True,default=None)
    etp_disk_ris = models.TextField(null=True,blank=True,default=None)
    dor_disk = models.TextField(null=True,blank=True,default=None)
    dor_disk_ris = models.TextField(null=True,blank=True,default=None)
    tgc_disk = models.TextField(null=True,blank=True,default=None)
    tgc_disk_ris = models.TextField(null=True,blank=True,default=None)
    col_disk = models.TextField(null=True,blank=True,default=None)
    col_disk_ris = models.TextField(null=True,blank=True,default=None)
    pol_disk = models.TextField(null=True,blank=True,default=None)
    pol_disk_ris = models.TextField(null=True,blank=True,default=None)
    dox_disk = models.TextField(null=True,blank=True,default=None)
    dox_disk_ris = models.TextField(null=True,blank=True,default=None)
    qda_disk = models.TextField(null=True,blank=True,default=None)
    qda_disk_ris = models.TextField(null=True,blank=True,default=None)
    mno_disk = models.TextField(null=True,blank=True,default=None)
    mno_disk_ris = models.TextField(null=True,blank=True,default=None)
    dap_disk = models.TextField(null=True,blank=True,default=None)
    dap_disk_ris = models.TextField(null=True,blank=True,default=None)
    comments = models.TextField(null=True,blank=True,default=None)
    
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred
    
    

class ArsrlMicResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amk_mic = models.TextField(null=True,blank=True,default=None)
    amk_mic_ris = models.TextField(null=True,blank=True,default=None)
    amc_mic = models.TextField(null=True,blank=True,default=None)
    amc_mic_ris = models.TextField(null=True,blank=True,default=None)
    amp_mic = models.TextField(null=True,blank=True,default=None)
    amp_mic_ris = models.TextField(null=True,blank=True,default=None)
    sam_mic = models.TextField(null=True,blank=True,default=None)
    sam_mic_ris = models.TextField(null=True,blank=True,default=None)
    atm_mic = models.TextField(null=True,blank=True,default=None)
    atm_mic_ris = models.TextField(null=True,blank=True,default=None)
    azm_mic = models.TextField(null=True,blank=True,default=None)
    azm_mic_ris = models.TextField(null=True,blank=True,default=None)
    cec_mic = models.TextField(null=True,blank=True,default=None)
    cec_mic_ris = models.TextField(null=True,blank=True,default=None)
    man_mic = models.TextField(null=True,blank=True,default=None)
    man_mic_ris = models.TextField(null=True,blank=True,default=None)
    czo_mic = models.TextField(null=True,blank=True,default=None)
    czo_mic_ris = models.TextField(null=True,blank=True,default=None)
    fep_mic = models.TextField(null=True,blank=True,default=None)
    fep_mic_ris = models.TextField(null=True,blank=True,default=None)
    cfm_mic = models.TextField(null=True,blank=True,default=None)
    cfm_mic_ris = models.TextField(null=True,blank=True,default=None)
    cfp_mic = models.TextField(null=True,blank=True,default=None)
    cfp_mic_ris = models.TextField(null=True,blank=True,default=None)
    ctx_mic = models.TextField(null=True,blank=True,default=None)
    ctx_mic_ris = models.TextField(null=True,blank=True,default=None)
    fox_mic = models.TextField(null=True,blank=True,default=None)
    fox_mic_ris = models.TextField(null=True,blank=True,default=None)
    caz_mic = models.TextField(null=True,blank=True,default=None)
    caz_mic_ris = models.TextField(null=True,blank=True,default=None)
    cro_mic = models.TextField(null=True,blank=True,default=None)
    cro_mic_ris = models.TextField(null=True,blank=True,default=None)
    cxa_mic = models.TextField(null=True,blank=True,default=None)
    cxa_mic_ris = models.TextField(null=True,blank=True,default=None)
    cep_mic = models.TextField(null=True,blank=True,default=None)
    cep_mic_ris = models.TextField(null=True,blank=True,default=None)
    chl_mic = models.TextField(null=True,blank=True,default=None)
    chl_mic_ris = models.TextField(null=True,blank=True,default=None)
    cip_mic = models.TextField(null=True,blank=True,default=None)
    cip_mic_ris = models.TextField(null=True,blank=True,default=None)
    clr_mic = models.TextField(null=True,blank=True,default=None)
    clr_mic_ris = models.TextField(null=True,blank=True,default=None)
    cli_mic = models.TextField(null=True,blank=True,default=None)
    cli_mic_ris = models.TextField(null=True,blank=True,default=None)
    sxt_mic = models.TextField(null=True,blank=True,default=None)
    sxt_mic_ris = models.TextField(null=True,blank=True,default=None)
    ery_mic = models.TextField(null=True,blank=True,default=None)
    ery_mic_ris = models.TextField(null=True,blank=True,default=None)
    gen_mic = models.TextField(null=True,blank=True,default=None)
    gen_mic_ris = models.TextField(null=True,blank=True,default=None)
    ipm_mic = models.TextField(null=True,blank=True,default=None)
    ipm_mic_ris = models.TextField(null=True,blank=True,default=None)
    kan_mic = models.TextField(null=True,blank=True,default=None)
    kan_mic_ris = models.TextField(null=True,blank=True,default=None)
    lev_mic = models.TextField(null=True,blank=True,default=None)
    lev_mic_ris = models.TextField(null=True,blank=True,default=None)
    nal_mic = models.TextField(null=True,blank=True,default=None)
    nal_mic_ris = models.TextField(null=True,blank=True,default=None)
    net_mic = models.TextField(null=True,blank=True,default=None)
    net_mic_ris = models.TextField(null=True,blank=True,default=None)
    nit_mic = models.TextField(null=True,blank=True,default=None)
    nit_mic_ris = models.TextField(null=True,blank=True,default=None)
    nor_mic = models.TextField(null=True,blank=True,default=None)
    nor_mic_ris = models.TextField(null=True,blank=True,default=None)
    ofx_mic = models.TextField(null=True,blank=True,default=None)
    ofx_mic_ris = models.TextField(null=True,blank=True,default=None)
    oxa_mic = models.TextField(null=True,blank=True,default=None)
    oxa_mic_ris = models.TextField(null=True,blank=True,default=None)
    pen_mic = models.TextField(null=True,blank=True,default=None)
    pen_mic_ris = models.TextField(null=True,blank=True,default=None)
    pip_mic = models.TextField(null=True,blank=True,default=None)
    pip_mic_ris = models.TextField(null=True,blank=True,default=None)
    rif_mic = models.TextField(null=True,blank=True,default=None)
    rif_mic_ris = models.TextField(null=True,blank=True,default=None)
    spe_mic = models.TextField(null=True,blank=True,default=None)
    spe_mic_ris = models.TextField(null=True,blank=True,default=None)
    str_mic = models.TextField(null=True,blank=True,default=None)
    str_mic_ris = models.TextField(null=True,blank=True,default=None)
    tet_mic = models.TextField(null=True,blank=True,default=None)
    tet_mic_ris = models.TextField(null=True,blank=True,default=None)
    tic_mic = models.TextField(null=True,blank=True,default=None)
    tic_mic_ris = models.TextField(null=True,blank=True,default=None)
    tcc_mic = models.TextField(null=True,blank=True,default=None)
    tcc_mic_ris = models.TextField(null=True,blank=True,default=None)
    tob_mic = models.TextField(null=True,blank=True,default=None)
    tob_mic_ris = models.TextField(null=True,blank=True,default=None)
    van_mic = models.TextField(null=True,blank=True,default=None)
    van_mic_ris = models.TextField(null=True,blank=True,default=None)
    mfx_mic = models.TextField(null=True,blank=True,default=None)
    mfx_mic_ris = models.TextField(null=True,blank=True,default=None)
    mem_mic = models.TextField(null=True,blank=True,default=None)
    mem_mic_ris = models.TextField(null=True,blank=True,default=None)
    tzp_mic = models.TextField(null=True,blank=True,default=None)
    tzp_mic_ris = models.TextField(null=True,blank=True,default=None)
    geh_mic = models.TextField(null=True,blank=True,default=None)
    geh_mic_ris = models.TextField(null=True,blank=True,default=None)
    sth_mic = models.TextField(null=True,blank=True,default=None)
    sth_mic_ris = models.TextField(null=True,blank=True,default=None)
    lnz_mic = models.TextField(null=True,blank=True,default=None)
    lnz_mic_ris = models.TextField(null=True,blank=True,default=None)
    nov_mic = models.TextField(null=True,blank=True,default=None)
    nov_mic_ris = models.TextField(null=True,blank=True,default=None)
    etp_mic = models.TextField(null=True,blank=True,default=None)
    etp_mic_ris = models.TextField(null=True,blank=True,default=None)
    dor_mic = models.TextField(null=True,blank=True,default=None)
    dor_mic_ris = models.TextField(null=True,blank=True,default=None)
    tgc_mic = models.TextField(null=True,blank=True,default=None)
    tgc_mic_ris = models.TextField(null=True,blank=True,default=None)
    col_mic = models.TextField(null=True,blank=True,default=None)
    col_mic_ris = models.TextField(null=True,blank=True,default=None)
    pol_mic = models.TextField(null=True,blank=True,default=None)
    pol_mic_ris = models.TextField(null=True,blank=True,default=None)
    dox_mic = models.TextField(null=True,blank=True,default=None)
    dox_mic_ris = models.TextField(null=True,blank=True,default=None)
    qda_mic = models.TextField(null=True,blank=True,default=None)
    qda_mic_ris = models.TextField(null=True,blank=True,default=None)
    mno_mic = models.TextField(null=True,blank=True,default=None)
    mno_mic_ris = models.TextField(null=True,blank=True,default=None)
    dap_mic = models.TextField(null=True,blank=True,default=None)
    dap_mic_ris = models.TextField(null=True,blank=True,default=None)
    
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.referred
    

class Process(models.Model):
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    process = models.TextField(null=True,blank=True,default=None)
    start_date = models.DateField(null=True,blank=True,default=None)
    start_sign = models.TextField(null=True,blank=True,default=None)
    finish_date = models.DateField(null=True,blank=True,default=None)
    finish_sign = models.TextField(null=True,blank=True,default=None)
    remarks = models.TextField(null=True,blank=True,default=None)
    running_tat = models.TextField(null=True,blank=True,default=None)
    days_completed = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process
    
    def get_format_date_start(self):
        if self.start_date != None:
            date_received = datetime.datetime.strftime(self.start_date, '%m/%d/%Y')
        else:
            date_received = None
        return date_received
    
    def finish_date_format(self):
        if self.finish_date != None:
            date_received = datetime.datetime.strftime(self.finish_date, '%m/%d/%Y')
        else:
            date_received = None
        return date_received

    
    def get_running_tat(self):
        batch = Batches.objects.get(id=self.batch_id)
        holidays = Holiday.objects.all().values_list('holiday',flat=True)
        diff = np.busday_count( batch.date_received,self.finish_date,holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
        return diff