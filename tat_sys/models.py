from django.db import models
import pandas as pd
import numpy as np
import datetime
from django.forms import model_to_dict
import uuid
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from datetime import date


dirpath = os.getcwd()

lab_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Lab')
dmu_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Dmu')
sec_staff = pd.read_excel(dirpath + '/tat_sys/static/excel_files/ARSP_STAFF.xlsx','Secretariat')

lab_staff = lab_staff['Staff Name'].values.tolist()
dmu_staff = dmu_staff['Staff Name'].values.tolist()
sec_staff = sec_staff['Staff Name'].values.tolist()
# Create your models here.


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=255,null=True,blank=True,default=None)
    hospital_code = models.CharField(max_length=255,null=True,blank=True,default=None)
    country = models.CharField(max_length=255,null=True,blank=True,default=None)
    island = models.CharField(max_length=255,null=True,blank=True,default=None)
    region = models.CharField(max_length=255,null=True,blank=True,default=None)
    province = models.CharField(max_length=255,null=True,blank=True,default=None)
    iso_3166_2 = models.CharField(max_length=255,null=True,blank=True,default=None)
    city = models.CharField(max_length=255,null=True,blank=True,default=None)
    latitude = models.CharField(max_length=255,null=True,blank=True,default=None)
    longitude = models.CharField(max_length=255,null=True,blank=True,default=None)
    address = models.TextField()
    history = HistoricalRecords()
    # other fields

    def __str__(self):
        return self.hospital_code


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    # other fields

    def __str__(self):
        return self.user.username
    
    def is_super_encoder(self):
        """Returns True if the user is in the 'SuperEncoder' group, False otherwise."""
        return self.user.groups.filter(name='SuperEncoder').exists()
    
    def is_site_encoder(self):
        """Returns True if the user is in the 'SiteEncoder' group, False otherwise."""
        return self.user.groups.filter(name='SiteEncoder').exists()
    
    def is_lab_encoder(self):
        """Returns True if the user is in the 'LabEncoder' group, False otherwise."""
        return self.user.groups.filter(name='LabEncoder').exists()

# class Packages(models.Model):
#     package_name = models.TextField(null=True,blank=True,default=None,unique=True)
#     site = models.TextField(max_length=3)
#     date_received = models.DateField()
#     received_by = models.TextField(max_length=99)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.package_name
    
#     def get_number_of_batches(self):
#         count = Batches.objects.filter(batch_name__startswith=self.package_name).count()
        
#         return count
        

# class Batches(models.Model):
#     batch_name = models.TextField(null=True,blank=True,default=None,unique=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#     site = models.TextField(max_length=3)
#     accession_number = models.TextField(max_length=99)
#     batch_number = models.IntegerField()
#     total_batch_number = models.IntegerField()
#     date_received = models.DateField()
#     received_by = models.TextField(max_length=99)
#     status = models.TextField(null=True,blank=True,default=None)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     @property
#     def get_reference_number(self):
#         s = self.accession_number
#         s = s.replace(" ","")
#         n = s.split("-")
#         count = Referred.objects.filter(batch=self.id).count()
#         return int(n[0]) + count
    
    
#     @property
#     def get_lab_number(self):
#         s = self.accession_number
#         s = s.replace(" ","")
#         n = s.split("-")
#         count = Referred.objects.filter(batch=self.id).count()
#         trailing_txt = "{:04d}".format(int(n[0]) + count)
#         year = datetime.date.today().strftime("%y")
#         return str(year) + 'ARS_' + str(self.site) + str(trailing_txt) 
    
    
#     @property
#     def number_of_isolate_encoded(self):
#         return Referred.objects.filter(batch=self.id).count()
        
    
    
#     @property
#     def number_of_isolates(self):
#         s = self.accession_number
#         s = s.replace(" ","")
#         n = s.split("-")
        
#         return (int(n[1]) - int(n[0])) + 1
    
    
#     @property
#     def get_current_status(self):
#         p = Process.objects.filter(batch_id=self.id).last()
#         ret = p.process
#         suff = ''
#         if p.finish_sign != None:
#             if p.finish_sign in lab_staff:
#                 suff = 'Lab'
#             elif p.finish_sign in sec_staff or p.finish_sign in dmu_staff:
#                 suff = 'Office'
            
            
#         else:
#             if p.start_sign in lab_staff:
#                 suff = 'Lab'
#             elif p.start_sign in sec_staff or p.start_sign in dmu_staff:
#                 suff = 'Office'
           
        
        
#         if '1_' in ret:
#             if suff != '':
#                 ret = 'Processing' + ' (' + suff + ')'
#             else:
#                 ret = 'Processing'
#         elif '2_' in ret:
#             if suff != '':
#                 ret = 'Encoding' + ' (' + suff + ')'
#             else:
#                 ret = 'Encoding'
#         elif '3_' in ret:
#             if suff != '':
#                 ret = 'Editing' + ' (' + suff + ')'
#             else:
#                 ret = 'Editing'
#         elif '4_' in ret:
#             if suff != '':
#                 ret = 'Lab Verification' + ' (' + suff + ')'
#             else:
#                 ret = 'Lab Verification'
#         elif '5_' in ret:
#             if suff != '':
#                 ret = 'Final Verification' + ' (' + suff + ')'
#             else:
#                 ret = 'Final Verification'
#         elif '6_' in ret:
#             if suff != '':
#                 ret = 'Releasing' + ' (' + suff + ')'
#             else:
#                 ret = 'Releasing'
            
#         return ret
   
   
#     @property
#     def get_running_tat(self):
#         holidays = Holiday.objects.all().values_list('holiday',flat=True)
#         diff = np.busday_count( self.date_received,datetime.date.today(),holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
#         return diff
    
    
  

#     def __str__(self):
#         return self.batch_name
    
    
    
    
#     def get_absolute_url(self):
#         return "batches/%i/" % self.id
    
#     @property
#     def get_encoding_url(self):
#         return "encoding/" + str(self.uuid) + '/'
    
#     @property
#     def get_qr_code_url(self):
#         return "http://10.10.25.178:8081/tat_sys/qr-code/" + str(self.uuid) + '/'
    
    
#     @property
#     def get_current_holder(self):
#         p = Process.objects.filter(batch_id=self.id).last()
#         suff = ''
#         if p.finish_sign != None:
#            suff = p.finish_sign  
#         else:
#             suff = p.start_sign
        
#         return suff
    
    
    
#     def get_format_date(self):
#         date_received = datetime.datetime.strftime(self.date_received, '%m/%d/%Y')
#         return date_received
    
#     def get_days_completed(self):
#         p = Process.objects.filter(batch_id=self.id)
#         p = p.exclude(days_completed=None)
#         p = p.values_list('days_completed', flat=True)
#         p = [int(i) for i in p] 
#         days_completed = sum(p)
        
#         return days_completed
    
#     def get_final_running_tat(self):
#         p = Process.objects.filter(batch_id=self.id).filter(process__startswith='6_lab_tech').last()
#         diff = '---'
#         if p != None:
#             if p.finish_date != None:
#                 batch = Batches.objects.get(id=self.id)
#                 holidays = Holiday.objects.all().values_list('holiday',flat=True)
#                 diff = np.busday_count( batch.date_received,p.finish_date,holidays=holidays,weekmask=[1,1,1,1,1,1,0])
          
               
#         return diff

  
        
        
        
        

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
    # batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    accession_number = models.TextField(max_length=99,null=True,blank=True,default=None)
    # reference_number = models.TextField(null=True,blank=True,default=None)
    # lab_number = models.TextField(null=True,blank=True,default=None)
    hospital_code = models.ForeignKey(Hospital, on_delete=models.CASCADE,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.TextField(null=True,blank=True,default=None)
    updated_by = models.TextField(null=True,blank=True,default=None)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.accession_number

    def clean(self):
        if self.accession_number and Referred.objects.filter(accession_number=self.accession_number).exists():
            raise ValidationError("Accession number must be unique.")
    
    
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

    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.first_name + " " + self.last_name

    def age(self):
        today = date.today()
        if self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        else:
            return None
    
    

class SiteIsolteInformation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    specimen_number = models.TextField(null=True,blank=True,default=None)
    specimen_date = models.DateField(null=True, blank=True,default=None)
    specimen_type = models.TextField(null=True,blank=True,default=None)
    reason_for_referral = models.TextField(null=True,blank=True,default=None)
    growth = models.TextField(null=True,blank=True,default=None)
    urine_count = models.TextField(null=True,blank=True,default=None)
    history = HistoricalRecords()
    
    
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
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.referred
    
    
    
class SiteOrganismResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    site_pre = models.TextField(null=True,blank=True,default=None)
    org_code = models.TextField(null=True,blank=True,default=None)
    org_site = models.TextField(null=True,blank=True,default=None)
    site_post = models.TextField(null=True,blank=True,default=None)
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.referred


class SiteDiskResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amc_nd20 = models.TextField(null=True,blank=True,default=None)
    amc_nd20_ris = models.TextField(null=True,blank=True,default=None)
    amk_nd30 = models.TextField(null=True,blank=True,default=None)
    amk_nd30_ris = models.TextField(null=True,blank=True,default=None)
    amp_nd10 = models.TextField(null=True,blank=True,default=None)
    amp_nd10_ris = models.TextField(null=True,blank=True,default=None)
    amx_nd30 = models.TextField(null=True,blank=True,default=None)
    amx_nd30_ris = models.TextField(null=True,blank=True,default=None)
    atm_nd30 = models.TextField(null=True,blank=True,default=None)
    atm_nd30_ris = models.TextField(null=True,blank=True,default=None)
    azm_nd15 = models.TextField(null=True,blank=True,default=None)
    azm_nd15_ris = models.TextField(null=True,blank=True,default=None)
    caz_nd30 = models.TextField(null=True,blank=True,default=None)
    caz_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cec_nd30 = models.TextField(null=True,blank=True,default=None)
    cec_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cep_nd30 = models.TextField(null=True,blank=True,default=None)
    cep_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cfm_nd5 = models.TextField(null=True,blank=True,default=None)
    cfm_nd5_ris = models.TextField(null=True,blank=True,default=None)
    cfp_nd75 = models.TextField(null=True,blank=True,default=None)
    cfp_nd75_ris = models.TextField(null=True,blank=True,default=None)
    chl_nd30 = models.TextField(null=True,blank=True,default=None)
    chl_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cip_nd5 = models.TextField(null=True,blank=True,default=None)
    cip_nd5_ris = models.TextField(null=True,blank=True,default=None)
    cli_nd2 = models.TextField(null=True,blank=True,default=None)
    cli_nd2_ris = models.TextField(null=True,blank=True,default=None)
    clr_nd15 = models.TextField(null=True,blank=True,default=None)
    clr_nd15_ris = models.TextField(null=True,blank=True,default=None)
    col_nd10 = models.TextField(null=True,blank=True,default=None)
    col_nd10_ris = models.TextField(null=True,blank=True,default=None)
    cro_nd30 = models.TextField(null=True,blank=True,default=None)
    cro_nd30_ris = models.TextField(null=True,blank=True,default=None)
    ctx_nd30 = models.TextField(null=True,blank=True,default=None)
    ctx_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cxa_nd30 = models.TextField(null=True,blank=True,default=None)
    cxa_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cxm_nd30 = models.TextField(null=True,blank=True,default=None)
    cxm_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cza_nd30 = models.TextField(null=True,blank=True,default=None)
    cza_nd30_ris = models.TextField(null=True,blank=True,default=None)
    czo_nd30 = models.TextField(null=True,blank=True,default=None)
    czo_nd30_ris = models.TextField(null=True,blank=True,default=None)
    czt_nd30 = models.TextField(null=True,blank=True,default=None)
    czt_nd30_ris = models.TextField(null=True,blank=True,default=None)
    dap_nd30 = models.TextField(null=True,blank=True,default=None)
    dap_nd30_ris = models.TextField(null=True,blank=True,default=None)
    dor_nd10 = models.TextField(null=True,blank=True,default=None)
    dor_nd10_ris = models.TextField(null=True,blank=True,default=None)
    dox_nd30 = models.TextField(null=True,blank=True,default=None)
    dox_nd30_ris = models.TextField(null=True,blank=True,default=None)
    ery_nd15 = models.TextField(null=True,blank=True,default=None)
    ery_nd15_ris = models.TextField(null=True,blank=True,default=None)
    etp_nd10 = models.TextField(null=True,blank=True,default=None)
    etp_nd10_ris = models.TextField(null=True,blank=True,default=None)
    fdc_nd = models.TextField(null=True,blank=True,default=None)
    fdc_nd_ris = models.TextField(null=True,blank=True,default=None)
    fep_nd30 = models.TextField(null=True,blank=True,default=None)
    fep_nd30_ris = models.TextField(null=True,blank=True,default=None)
    fos_nd200 = models.TextField(null=True,blank=True,default=None)
    fos_nd200_ris = models.TextField(null=True,blank=True,default=None)
    fox_nd30 = models.TextField(null=True,blank=True,default=None)
    fox_nd30_ris = models.TextField(null=True,blank=True,default=None)
    geh_nd120 = models.TextField(null=True,blank=True,default=None)
    geh_nd120_ris = models.TextField(null=True,blank=True,default=None)
    gen_nd10 = models.TextField(null=True,blank=True,default=None)
    gen_nd10_ris = models.TextField(null=True,blank=True,default=None)
    imr_nd10 = models.TextField(null=True,blank=True,default=None)
    imr_nd10_ris = models.TextField(null=True,blank=True,default=None)
    ipm_nd10 = models.TextField(null=True,blank=True,default=None)
    ipm_nd10_ris = models.TextField(null=True,blank=True,default=None)
    kan_nd30 = models.TextField(null=True,blank=True,default=None)
    kan_nd30_ris = models.TextField(null=True,blank=True,default=None)
    lnz_nd30 = models.TextField(null=True,blank=True,default=None)
    lnz_nd30_ris = models.TextField(null=True,blank=True,default=None)
    lvx_nd5 = models.TextField(null=True,blank=True,default=None)
    lvx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    man_nd30 = models.TextField(null=True,blank=True,default=None)
    man_nd30_ris = models.TextField(null=True,blank=True,default=None)
    mem_nd10 = models.TextField(null=True,blank=True,default=None)
    mem_nd10_ris = models.TextField(null=True,blank=True,default=None)
    mev_nd20 = models.TextField(null=True,blank=True,default=None)
    mev_nd20_ris = models.TextField(null=True,blank=True,default=None)
    mfx_nd5 = models.TextField(null=True,blank=True,default=None)
    mfx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    mno_nd30 = models.TextField(null=True,blank=True,default=None)
    mno_nd30_ris = models.TextField(null=True,blank=True,default=None)
    nal_nd30 = models.TextField(null=True,blank=True,default=None)
    nal_nd30_ris = models.TextField(null=True,blank=True,default=None)
    net_nd30 = models.TextField(null=True,blank=True,default=None)
    net_nd30_ris = models.TextField(null=True,blank=True,default=None)
    nit_nd300 = models.TextField(null=True,blank=True,default=None)
    nit_nd300_ris = models.TextField(null=True,blank=True,default=None)
    nor_nd10 = models.TextField(null=True,blank=True,default=None)
    nor_nd10_ris = models.TextField(null=True,blank=True,default=None)
    nov_nd5 = models.TextField(null=True,blank=True,default=None)
    nov_nd5_ris = models.TextField(null=True,blank=True,default=None)
    ofx_nd5 = models.TextField(null=True,blank=True,default=None)
    ofx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    oxa_nd1 = models.TextField(null=True,blank=True,default=None)
    oxa_nd1_ris = models.TextField(null=True,blank=True,default=None)
    pen_nd10 = models.TextField(null=True,blank=True,default=None)
    pen_nd10_ris = models.TextField(null=True,blank=True,default=None)
    pip_nd100 = models.TextField(null=True,blank=True,default=None)
    pip_nd100_ris = models.TextField(null=True,blank=True,default=None)
    plz_nd = models.TextField(null=True,blank=True,default=None)
    plz_nd_ris = models.TextField(null=True,blank=True,default=None)
    pol_nd300 = models.TextField(null=True,blank=True,default=None)
    pol_nd300_ris = models.TextField(null=True,blank=True,default=None)
    qda_nd15 = models.TextField(null=True,blank=True,default=None)
    qda_nd15_ris = models.TextField(null=True,blank=True,default=None)
    rif_nd5 = models.TextField(null=True,blank=True,default=None)
    rif_nd5_ris = models.TextField(null=True,blank=True,default=None)
    sam_nd10 = models.TextField(null=True,blank=True,default=None)
    sam_nd10_ris = models.TextField(null=True,blank=True,default=None)
    spt_nd100 = models.TextField(null=True,blank=True,default=None)
    spt_nd100_ris = models.TextField(null=True,blank=True,default=None)
    sss_nd200 = models.TextField(null=True,blank=True,default=None)
    sss_nd200_ris = models.TextField(null=True,blank=True,default=None)
    sth_nd300 = models.TextField(null=True,blank=True,default=None)
    sth_nd300_ris = models.TextField(null=True,blank=True,default=None)
    str_nd10 = models.TextField(null=True,blank=True,default=None)
    str_nd10_ris = models.TextField(null=True,blank=True,default=None)
    sxt_nd1_2 = models.TextField(null=True,blank=True,default=None)
    sxt_nd1_2_ris = models.TextField(null=True,blank=True,default=None)
    tcc_nd75 = models.TextField(null=True,blank=True,default=None)
    tcc_nd75_ris = models.TextField(null=True,blank=True,default=None)
    tcy_nd30 = models.TextField(null=True,blank=True,default=None)
    tcy_nd30_ris = models.TextField(null=True,blank=True,default=None)
    tgc_nd15 = models.TextField(null=True,blank=True,default=None)
    tgc_nd15_ris = models.TextField(null=True,blank=True,default=None)
    tic_nd75 = models.TextField(null=True,blank=True,default=None)
    tic_nd75_ris = models.TextField(null=True,blank=True,default=None)
    tob_nd10 = models.TextField(null=True,blank=True,default=None)
    tob_nd10_ris = models.TextField(null=True,blank=True,default=None)
    tzd_nd = models.TextField(null=True,blank=True,default=None)
    tzd_nd_ris = models.TextField(null=True,blank=True,default=None)
    tzp_nd100 = models.TextField(null=True,blank=True,default=None)
    tzp_nd100_ris = models.TextField(null=True,blank=True,default=None)
    van_nd30 = models.TextField(null=True,blank=True,default=None)
    van_nd30_ris = models.TextField(null=True,blank=True,default=None)

    amb_nd10 = models.TextField(null=True,blank=True,default=None)
    amb_nd10_ris = models.TextField(null=True,blank=True,default=None)
    cpt_nd30 = models.TextField(null=True,blank=True,default=None)
    cpt_nd30_ris = models.TextField(null=True,blank=True,default=None)
    fct_nd10 = models.TextField(null=True,blank=True,default=None)
    fct_nd10_ris = models.TextField(null=True,blank=True,default=None)
    pri_nd15 = models.TextField(null=True,blank=True,default=None)
    pri_nd15_ris = models.TextField(null=True,blank=True,default=None)
    spx_nd5 = models.TextField(null=True,blank=True,default=None)
    spx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    tec_nd30 = models.TextField(null=True,blank=True,default=None)
    tec_nd30_ris = models.TextField(null=True,blank=True,default=None)
    tlt_nd15 = models.TextField(null=True,blank=True,default=None)
    tlt_nd15_ris = models.TextField(null=True,blank=True,default=None)



    
    comments = models.TextField(null=True,blank=True,default=None)
    
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.referred
    
    

class SiteMicResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amc_nm = models.TextField(null=True,blank=True,default=None)
    amc_nm_ris = models.TextField(null=True,blank=True,default=None)
    amk_nm = models.TextField(null=True,blank=True,default=None)
    amk_nm_ris = models.TextField(null=True,blank=True,default=None)
    amp_nm = models.TextField(null=True,blank=True,default=None)
    amp_nm_ris = models.TextField(null=True,blank=True,default=None)
    amx_nm = models.TextField(null=True,blank=True,default=None)
    amx_nm_ris = models.TextField(null=True,blank=True,default=None)
    atm_nm = models.TextField(null=True,blank=True,default=None)
    atm_nm_ris = models.TextField(null=True,blank=True,default=None)
    azm_nm = models.TextField(null=True,blank=True,default=None)
    azm_nm_ris = models.TextField(null=True,blank=True,default=None)
    caz_nm = models.TextField(null=True,blank=True,default=None)
    caz_nm_ris = models.TextField(null=True,blank=True,default=None)
    cec_nm = models.TextField(null=True,blank=True,default=None)
    cec_nm_ris = models.TextField(null=True,blank=True,default=None)
    cep_nm = models.TextField(null=True,blank=True,default=None)
    cep_nm_ris = models.TextField(null=True,blank=True,default=None)
    cfm_nm = models.TextField(null=True,blank=True,default=None)
    cfm_nm_ris = models.TextField(null=True,blank=True,default=None)
    cfp_nm = models.TextField(null=True,blank=True,default=None)
    cfp_nm_ris = models.TextField(null=True,blank=True,default=None)
    chl_nm = models.TextField(null=True,blank=True,default=None)
    chl_nm_ris = models.TextField(null=True,blank=True,default=None)
    cip_nm = models.TextField(null=True,blank=True,default=None)
    cip_nm_ris = models.TextField(null=True,blank=True,default=None)
    cli_nm = models.TextField(null=True,blank=True,default=None)
    cli_nm_ris = models.TextField(null=True,blank=True,default=None)
    clr_nm = models.TextField(null=True,blank=True,default=None)
    clr_nm_ris = models.TextField(null=True,blank=True,default=None)
    col_nm = models.TextField(null=True,blank=True,default=None)
    col_nm_ris = models.TextField(null=True,blank=True,default=None)
    cro_nm = models.TextField(null=True,blank=True,default=None)
    cro_nm_ris = models.TextField(null=True,blank=True,default=None)
    ctx_nm = models.TextField(null=True,blank=True,default=None)
    ctx_nm_ris = models.TextField(null=True,blank=True,default=None)
    cxa_nm = models.TextField(null=True,blank=True,default=None)
    cxa_nm_ris = models.TextField(null=True,blank=True,default=None)
    cxm_nm = models.TextField(null=True,blank=True,default=None)
    cxm_nm_ris = models.TextField(null=True,blank=True,default=None)
    cza_nm = models.TextField(null=True,blank=True,default=None)
    cza_nm_ris = models.TextField(null=True,blank=True,default=None)
    czo_nm = models.TextField(null=True,blank=True,default=None)
    czo_nm_ris = models.TextField(null=True,blank=True,default=None)
    czt_nm = models.TextField(null=True,blank=True,default=None)
    czt_nm_ris = models.TextField(null=True,blank=True,default=None)
    dap_nm = models.TextField(null=True,blank=True,default=None)
    dap_nm_ris = models.TextField(null=True,blank=True,default=None)
    dor_nm = models.TextField(null=True,blank=True,default=None)
    dor_nm_ris = models.TextField(null=True,blank=True,default=None)
    dox_nm = models.TextField(null=True,blank=True,default=None)
    dox_nm_ris = models.TextField(null=True,blank=True,default=None)
    ery_nm = models.TextField(null=True,blank=True,default=None)
    ery_nm_ris = models.TextField(null=True,blank=True,default=None)
    etp_nm = models.TextField(null=True,blank=True,default=None)
    etp_nm_ris = models.TextField(null=True,blank=True,default=None)
    fdc_nm = models.TextField(null=True,blank=True,default=None)
    fdc_nm_ris = models.TextField(null=True,blank=True,default=None)
    fep_nm = models.TextField(null=True,blank=True,default=None)
    fep_nm_ris = models.TextField(null=True,blank=True,default=None)
    fos_nm = models.TextField(null=True,blank=True,default=None)
    fos_nm_ris = models.TextField(null=True,blank=True,default=None)
    fox_nm = models.TextField(null=True,blank=True,default=None)
    fox_nm_ris = models.TextField(null=True,blank=True,default=None)
    geh_nm = models.TextField(null=True,blank=True,default=None)
    geh_nm_ris = models.TextField(null=True,blank=True,default=None)
    gen_nm = models.TextField(null=True,blank=True,default=None)
    gen_nm_ris = models.TextField(null=True,blank=True,default=None)
    imr_nm = models.TextField(null=True,blank=True,default=None)
    imr_nm_ris = models.TextField(null=True,blank=True,default=None)
    ipm_nm = models.TextField(null=True,blank=True,default=None)
    ipm_nm_ris = models.TextField(null=True,blank=True,default=None)
    kan_nm = models.TextField(null=True,blank=True,default=None)
    kan_nm_ris = models.TextField(null=True,blank=True,default=None)
    lnz_nm = models.TextField(null=True,blank=True,default=None)
    lnz_nm_ris = models.TextField(null=True,blank=True,default=None)
    lvx_nm = models.TextField(null=True,blank=True,default=None)
    lvx_nm_ris = models.TextField(null=True,blank=True,default=None)
    man_nm = models.TextField(null=True,blank=True,default=None)
    man_nm_ris = models.TextField(null=True,blank=True,default=None)
    mem_nm = models.TextField(null=True,blank=True,default=None)
    mem_nm_ris = models.TextField(null=True,blank=True,default=None)
    mev_nm = models.TextField(null=True,blank=True,default=None)
    mev_nm_ris = models.TextField(null=True,blank=True,default=None)
    mfx_nm = models.TextField(null=True,blank=True,default=None)
    mfx_nm_ris = models.TextField(null=True,blank=True,default=None)
    mno_nm = models.TextField(null=True,blank=True,default=None)
    mno_nm_ris = models.TextField(null=True,blank=True,default=None)
    nal_nm = models.TextField(null=True,blank=True,default=None)
    nal_nm_ris = models.TextField(null=True,blank=True,default=None)
    net_nm = models.TextField(null=True,blank=True,default=None)
    net_nm_ris = models.TextField(null=True,blank=True,default=None)
    nit_nm = models.TextField(null=True,blank=True,default=None)
    nit_nm_ris = models.TextField(null=True,blank=True,default=None)
    nor_nm = models.TextField(null=True,blank=True,default=None)
    nor_nm_ris = models.TextField(null=True,blank=True,default=None)
    nov_nm = models.TextField(null=True,blank=True,default=None)
    nov_nm_ris = models.TextField(null=True,blank=True,default=None)
    ofx_nm = models.TextField(null=True,blank=True,default=None)
    ofx_nm_ris = models.TextField(null=True,blank=True,default=None)
    oxa_nm = models.TextField(null=True,blank=True,default=None)
    oxa_nm_ris = models.TextField(null=True,blank=True,default=None)
    pen_nm = models.TextField(null=True,blank=True,default=None)
    pen_nm_ris = models.TextField(null=True,blank=True,default=None)
    pip_nm = models.TextField(null=True,blank=True,default=None)
    pip_nm_ris = models.TextField(null=True,blank=True,default=None)
    plz_nm = models.TextField(null=True,blank=True,default=None)
    plz_nm_ris = models.TextField(null=True,blank=True,default=None)
    pol_nm = models.TextField(null=True,blank=True,default=None)
    pol_nm_ris = models.TextField(null=True,blank=True,default=None)
    qda_nm = models.TextField(null=True,blank=True,default=None)
    qda_nm_ris = models.TextField(null=True,blank=True,default=None)
    rif_nm = models.TextField(null=True,blank=True,default=None)
    rif_nm_ris = models.TextField(null=True,blank=True,default=None)
    sam_nm = models.TextField(null=True,blank=True,default=None)
    sam_nm_ris = models.TextField(null=True,blank=True,default=None)
    spt_nm = models.TextField(null=True,blank=True,default=None)
    spt_nm_ris = models.TextField(null=True,blank=True,default=None)
    sss_nm = models.TextField(null=True,blank=True,default=None)
    sss_nm_ris = models.TextField(null=True,blank=True,default=None)
    sth_nm = models.TextField(null=True,blank=True,default=None)
    sth_nm_ris = models.TextField(null=True,blank=True,default=None)
    str_nm = models.TextField(null=True,blank=True,default=None)
    str_nm_ris = models.TextField(null=True,blank=True,default=None)
    sxt_nm = models.TextField(null=True,blank=True,default=None)
    sxt_nm_ris = models.TextField(null=True,blank=True,default=None)
    tcc_nm = models.TextField(null=True,blank=True,default=None)
    tcc_nm_ris = models.TextField(null=True,blank=True,default=None)
    tcy_nm = models.TextField(null=True,blank=True,default=None)
    tcy_nm_ris = models.TextField(null=True,blank=True,default=None)
    tgc_nm = models.TextField(null=True,blank=True,default=None)
    tgc_nm_ris = models.TextField(null=True,blank=True,default=None)
    tic_nm = models.TextField(null=True,blank=True,default=None)
    tic_nm_ris = models.TextField(null=True,blank=True,default=None)
    tob_nm = models.TextField(null=True,blank=True,default=None)
    tob_nm_ris = models.TextField(null=True,blank=True,default=None)
    tzd_nm = models.TextField(null=True,blank=True,default=None)
    tzd_nm_ris = models.TextField(null=True,blank=True,default=None)
    tzp_nm = models.TextField(null=True,blank=True,default=None)
    tzp_nm_ris = models.TextField(null=True,blank=True,default=None)
    van_nm = models.TextField(null=True,blank=True,default=None)
    van_nm_ris = models.TextField(null=True,blank=True,default=None)


    amb_nm = models.TextField(null=True,blank=True,default=None)
    amb_nm_ris = models.TextField(null=True,blank=True,default=None)
    cpt_nm = models.TextField(null=True,blank=True,default=None)
    cpt_nm_ris = models.TextField(null=True,blank=True,default=None)
    fct_nm = models.TextField(null=True,blank=True,default=None)
    fct_nm_ris = models.TextField(null=True,blank=True,default=None)
    pri_nm = models.TextField(null=True,blank=True,default=None)
    pri_nm_ris = models.TextField(null=True,blank=True,default=None)
    spx_nm = models.TextField(null=True,blank=True,default=None)
    spx_nm_ris = models.TextField(null=True,blank=True,default=None)
    tec_nm = models.TextField(null=True,blank=True,default=None)
    tec_nm_ris = models.TextField(null=True,blank=True,default=None)
    tlt_nm = models.TextField(null=True,blank=True,default=None)
    tlt_nm_ris = models.TextField(null=True,blank=True,default=None)
    
    history = HistoricalRecords()
    
    
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
    
    history = HistoricalRecords()



class ArsrlRecommendation(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    recommendation_code = models.TextField(null=True,blank=True,default=None)
    recommendation = models.TextField(null=True,blank=True,default=None)
    description = models.TextField(null=True,blank=True,default=None)


    history = HistoricalRecords()




class ArsrlDiskResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amc_nd20 = models.TextField(null=True,blank=True,default=None)
    amc_nd20_ris = models.TextField(null=True,blank=True,default=None)
    amk_nd30 = models.TextField(null=True,blank=True,default=None)
    amk_nd30_ris = models.TextField(null=True,blank=True,default=None)
    amp_nd10 = models.TextField(null=True,blank=True,default=None)
    amp_nd10_ris = models.TextField(null=True,blank=True,default=None)
    amx_nd30 = models.TextField(null=True,blank=True,default=None)
    amx_nd30_ris = models.TextField(null=True,blank=True,default=None)
    atm_nd30 = models.TextField(null=True,blank=True,default=None)
    atm_nd30_ris = models.TextField(null=True,blank=True,default=None)
    azm_nd15 = models.TextField(null=True,blank=True,default=None)
    azm_nd15_ris = models.TextField(null=True,blank=True,default=None)
    caz_nd30 = models.TextField(null=True,blank=True,default=None)
    caz_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cec_nd30 = models.TextField(null=True,blank=True,default=None)
    cec_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cep_nd30 = models.TextField(null=True,blank=True,default=None)
    cep_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cfm_nd5 = models.TextField(null=True,blank=True,default=None)
    cfm_nd5_ris = models.TextField(null=True,blank=True,default=None)
    cfp_nd75 = models.TextField(null=True,blank=True,default=None)
    cfp_nd75_ris = models.TextField(null=True,blank=True,default=None)
    chl_nd30 = models.TextField(null=True,blank=True,default=None)
    chl_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cip_nd5 = models.TextField(null=True,blank=True,default=None)
    cip_nd5_ris = models.TextField(null=True,blank=True,default=None)
    cli_nd2 = models.TextField(null=True,blank=True,default=None)
    cli_nd2_ris = models.TextField(null=True,blank=True,default=None)
    clr_nd15 = models.TextField(null=True,blank=True,default=None)
    clr_nd15_ris = models.TextField(null=True,blank=True,default=None)
    col_nd10 = models.TextField(null=True,blank=True,default=None)
    col_nd10_ris = models.TextField(null=True,blank=True,default=None)
    cro_nd30 = models.TextField(null=True,blank=True,default=None)
    cro_nd30_ris = models.TextField(null=True,blank=True,default=None)
    ctx_nd30 = models.TextField(null=True,blank=True,default=None)
    ctx_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cxa_nd30 = models.TextField(null=True,blank=True,default=None)
    cxa_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cxm_nd30 = models.TextField(null=True,blank=True,default=None)
    cxm_nd30_ris = models.TextField(null=True,blank=True,default=None)
    cza_nd30 = models.TextField(null=True,blank=True,default=None)
    cza_nd30_ris = models.TextField(null=True,blank=True,default=None)
    czo_nd30 = models.TextField(null=True,blank=True,default=None)
    czo_nd30_ris = models.TextField(null=True,blank=True,default=None)
    czt_nd30 = models.TextField(null=True,blank=True,default=None)
    czt_nd30_ris = models.TextField(null=True,blank=True,default=None)
    dap_nd30 = models.TextField(null=True,blank=True,default=None)
    dap_nd30_ris = models.TextField(null=True,blank=True,default=None)
    dor_nd10 = models.TextField(null=True,blank=True,default=None)
    dor_nd10_ris = models.TextField(null=True,blank=True,default=None)
    dox_nd30 = models.TextField(null=True,blank=True,default=None)
    dox_nd30_ris = models.TextField(null=True,blank=True,default=None)
    ery_nd15 = models.TextField(null=True,blank=True,default=None)
    ery_nd15_ris = models.TextField(null=True,blank=True,default=None)
    etp_nd10 = models.TextField(null=True,blank=True,default=None)
    etp_nd10_ris = models.TextField(null=True,blank=True,default=None)
    fdc_nd = models.TextField(null=True,blank=True,default=None)
    fdc_nd_ris = models.TextField(null=True,blank=True,default=None)
    fep_nd30 = models.TextField(null=True,blank=True,default=None)
    fep_nd30_ris = models.TextField(null=True,blank=True,default=None)
    fos_nd200 = models.TextField(null=True,blank=True,default=None)
    fos_nd200_ris = models.TextField(null=True,blank=True,default=None)
    fox_nd30 = models.TextField(null=True,blank=True,default=None)
    fox_nd30_ris = models.TextField(null=True,blank=True,default=None)
    geh_nd120 = models.TextField(null=True,blank=True,default=None)
    geh_nd120_ris = models.TextField(null=True,blank=True,default=None)
    gen_nd10 = models.TextField(null=True,blank=True,default=None)
    gen_nd10_ris = models.TextField(null=True,blank=True,default=None)
    imr_nd10 = models.TextField(null=True,blank=True,default=None)
    imr_nd10_ris = models.TextField(null=True,blank=True,default=None)
    ipm_nd10 = models.TextField(null=True,blank=True,default=None)
    ipm_nd10_ris = models.TextField(null=True,blank=True,default=None)
    kan_nd30 = models.TextField(null=True,blank=True,default=None)
    kan_nd30_ris = models.TextField(null=True,blank=True,default=None)
    lnz_nd30 = models.TextField(null=True,blank=True,default=None)
    lnz_nd30_ris = models.TextField(null=True,blank=True,default=None)
    lvx_nd5 = models.TextField(null=True,blank=True,default=None)
    lvx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    man_nd30 = models.TextField(null=True,blank=True,default=None)
    man_nd30_ris = models.TextField(null=True,blank=True,default=None)
    mem_nd10 = models.TextField(null=True,blank=True,default=None)
    mem_nd10_ris = models.TextField(null=True,blank=True,default=None)
    mev_nd20 = models.TextField(null=True,blank=True,default=None)
    mev_nd20_ris = models.TextField(null=True,blank=True,default=None)
    mfx_nd5 = models.TextField(null=True,blank=True,default=None)
    mfx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    mno_nd30 = models.TextField(null=True,blank=True,default=None)
    mno_nd30_ris = models.TextField(null=True,blank=True,default=None)
    nal_nd30 = models.TextField(null=True,blank=True,default=None)
    nal_nd30_ris = models.TextField(null=True,blank=True,default=None)
    net_nd30 = models.TextField(null=True,blank=True,default=None)
    net_nd30_ris = models.TextField(null=True,blank=True,default=None)
    nit_nd300 = models.TextField(null=True,blank=True,default=None)
    nit_nd300_ris = models.TextField(null=True,blank=True,default=None)
    nor_nd10 = models.TextField(null=True,blank=True,default=None)
    nor_nd10_ris = models.TextField(null=True,blank=True,default=None)
    nov_nd5 = models.TextField(null=True,blank=True,default=None)
    nov_nd5_ris = models.TextField(null=True,blank=True,default=None)
    ofx_nd5 = models.TextField(null=True,blank=True,default=None)
    ofx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    oxa_nd1 = models.TextField(null=True,blank=True,default=None)
    oxa_nd1_ris = models.TextField(null=True,blank=True,default=None)
    pen_nd10 = models.TextField(null=True,blank=True,default=None)
    pen_nd10_ris = models.TextField(null=True,blank=True,default=None)
    pip_nd100 = models.TextField(null=True,blank=True,default=None)
    pip_nd100_ris = models.TextField(null=True,blank=True,default=None)
    plz_nd = models.TextField(null=True,blank=True,default=None)
    plz_nd_ris = models.TextField(null=True,blank=True,default=None)
    pol_nd300 = models.TextField(null=True,blank=True,default=None)
    pol_nd300_ris = models.TextField(null=True,blank=True,default=None)
    qda_nd15 = models.TextField(null=True,blank=True,default=None)
    qda_nd15_ris = models.TextField(null=True,blank=True,default=None)
    rif_nd5 = models.TextField(null=True,blank=True,default=None)
    rif_nd5_ris = models.TextField(null=True,blank=True,default=None)
    sam_nd10 = models.TextField(null=True,blank=True,default=None)
    sam_nd10_ris = models.TextField(null=True,blank=True,default=None)
    spt_nd100 = models.TextField(null=True,blank=True,default=None)
    spt_nd100_ris = models.TextField(null=True,blank=True,default=None)
    sss_nd200 = models.TextField(null=True,blank=True,default=None)
    sss_nd200_ris = models.TextField(null=True,blank=True,default=None)
    sth_nd300 = models.TextField(null=True,blank=True,default=None)
    sth_nd300_ris = models.TextField(null=True,blank=True,default=None)
    str_nd10 = models.TextField(null=True,blank=True,default=None)
    str_nd10_ris = models.TextField(null=True,blank=True,default=None)
    sxt_nd1_2 = models.TextField(null=True,blank=True,default=None)
    sxt_nd1_2_ris = models.TextField(null=True,blank=True,default=None)
    tcc_nd75 = models.TextField(null=True,blank=True,default=None)
    tcc_nd75_ris = models.TextField(null=True,blank=True,default=None)
    tcy_nd30 = models.TextField(null=True,blank=True,default=None)
    tcy_nd30_ris = models.TextField(null=True,blank=True,default=None)
    tgc_nd15 = models.TextField(null=True,blank=True,default=None)
    tgc_nd15_ris = models.TextField(null=True,blank=True,default=None)
    tic_nd75 = models.TextField(null=True,blank=True,default=None)
    tic_nd75_ris = models.TextField(null=True,blank=True,default=None)
    tob_nd10 = models.TextField(null=True,blank=True,default=None)
    tob_nd10_ris = models.TextField(null=True,blank=True,default=None)
    tzd_nd = models.TextField(null=True,blank=True,default=None)
    tzd_nd_ris = models.TextField(null=True,blank=True,default=None)
    tzp_nd100 = models.TextField(null=True,blank=True,default=None)
    tzp_nd100_ris = models.TextField(null=True,blank=True,default=None)
    van_nd30 = models.TextField(null=True,blank=True,default=None)
    van_nd30_ris = models.TextField(null=True,blank=True,default=None)

    amb_nd10 = models.TextField(null=True,blank=True,default=None)
    amb_nd10_ris = models.TextField(null=True,blank=True,default=None)
    cpt_nd30 = models.TextField(null=True,blank=True,default=None)
    cpt_nd30_ris = models.TextField(null=True,blank=True,default=None)
    fct_nd10 = models.TextField(null=True,blank=True,default=None)
    fct_nd10_ris = models.TextField(null=True,blank=True,default=None)
    pri_nd15 = models.TextField(null=True,blank=True,default=None)
    pri_nd15_ris = models.TextField(null=True,blank=True,default=None)
    spx_nd5 = models.TextField(null=True,blank=True,default=None)
    spx_nd5_ris = models.TextField(null=True,blank=True,default=None)
    tec_nd30 = models.TextField(null=True,blank=True,default=None)
    tec_nd30_ris = models.TextField(null=True,blank=True,default=None)
    tlt_nd15 = models.TextField(null=True,blank=True,default=None)
    tlt_nd15_ris = models.TextField(null=True,blank=True,default=None)

    comments = models.TextField(null=True,blank=True,default=None)
    


    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.referred
    
    

class ArsrlMicResult(models.Model):
    referred = models.ForeignKey(Referred, on_delete=models.CASCADE)
    amc_nm = models.TextField(null=True,blank=True,default=None)
    amc_nm_ris = models.TextField(null=True,blank=True,default=None)
    amk_nm = models.TextField(null=True,blank=True,default=None)
    amk_nm_ris = models.TextField(null=True,blank=True,default=None)
    amp_nm = models.TextField(null=True,blank=True,default=None)
    amp_nm_ris = models.TextField(null=True,blank=True,default=None)
    amx_nm = models.TextField(null=True,blank=True,default=None)
    amx_nm_ris = models.TextField(null=True,blank=True,default=None)
    atm_nm = models.TextField(null=True,blank=True,default=None)
    atm_nm_ris = models.TextField(null=True,blank=True,default=None)
    azm_nm = models.TextField(null=True,blank=True,default=None)
    azm_nm_ris = models.TextField(null=True,blank=True,default=None)
    caz_nm = models.TextField(null=True,blank=True,default=None)
    caz_nm_ris = models.TextField(null=True,blank=True,default=None)
    cec_nm = models.TextField(null=True,blank=True,default=None)
    cec_nm_ris = models.TextField(null=True,blank=True,default=None)
    cep_nm = models.TextField(null=True,blank=True,default=None)
    cep_nm_ris = models.TextField(null=True,blank=True,default=None)
    cfm_nm = models.TextField(null=True,blank=True,default=None)
    cfm_nm_ris = models.TextField(null=True,blank=True,default=None)
    cfp_nm = models.TextField(null=True,blank=True,default=None)
    cfp_nm_ris = models.TextField(null=True,blank=True,default=None)
    chl_nm = models.TextField(null=True,blank=True,default=None)
    chl_nm_ris = models.TextField(null=True,blank=True,default=None)
    cip_nm = models.TextField(null=True,blank=True,default=None)
    cip_nm_ris = models.TextField(null=True,blank=True,default=None)
    cli_nm = models.TextField(null=True,blank=True,default=None)
    cli_nm_ris = models.TextField(null=True,blank=True,default=None)
    clr_nm = models.TextField(null=True,blank=True,default=None)
    clr_nm_ris = models.TextField(null=True,blank=True,default=None)
    col_nm = models.TextField(null=True,blank=True,default=None)
    col_nm_ris = models.TextField(null=True,blank=True,default=None)
    cro_nm = models.TextField(null=True,blank=True,default=None)
    cro_nm_ris = models.TextField(null=True,blank=True,default=None)
    ctx_nm = models.TextField(null=True,blank=True,default=None)
    ctx_nm_ris = models.TextField(null=True,blank=True,default=None)
    cxa_nm = models.TextField(null=True,blank=True,default=None)
    cxa_nm_ris = models.TextField(null=True,blank=True,default=None)
    cxm_nm = models.TextField(null=True,blank=True,default=None)
    cxm_nm_ris = models.TextField(null=True,blank=True,default=None)
    cza_nm = models.TextField(null=True,blank=True,default=None)
    cza_nm_ris = models.TextField(null=True,blank=True,default=None)
    czo_nm = models.TextField(null=True,blank=True,default=None)
    czo_nm_ris = models.TextField(null=True,blank=True,default=None)
    czt_nm = models.TextField(null=True,blank=True,default=None)
    czt_nm_ris = models.TextField(null=True,blank=True,default=None)
    dap_nm = models.TextField(null=True,blank=True,default=None)
    dap_nm_ris = models.TextField(null=True,blank=True,default=None)
    dor_nm = models.TextField(null=True,blank=True,default=None)
    dor_nm_ris = models.TextField(null=True,blank=True,default=None)
    dox_nm = models.TextField(null=True,blank=True,default=None)
    dox_nm_ris = models.TextField(null=True,blank=True,default=None)
    ery_nm = models.TextField(null=True,blank=True,default=None)
    ery_nm_ris = models.TextField(null=True,blank=True,default=None)
    etp_nm = models.TextField(null=True,blank=True,default=None)
    etp_nm_ris = models.TextField(null=True,blank=True,default=None)
    fdc_nm = models.TextField(null=True,blank=True,default=None)
    fdc_nm_ris = models.TextField(null=True,blank=True,default=None)
    fep_nm = models.TextField(null=True,blank=True,default=None)
    fep_nm_ris = models.TextField(null=True,blank=True,default=None)
    fos_nm = models.TextField(null=True,blank=True,default=None)
    fos_nm_ris = models.TextField(null=True,blank=True,default=None)
    fox_nm = models.TextField(null=True,blank=True,default=None)
    fox_nm_ris = models.TextField(null=True,blank=True,default=None)
    geh_nm = models.TextField(null=True,blank=True,default=None)
    geh_nm_ris = models.TextField(null=True,blank=True,default=None)
    gen_nm = models.TextField(null=True,blank=True,default=None)
    gen_nm_ris = models.TextField(null=True,blank=True,default=None)
    imr_nm = models.TextField(null=True,blank=True,default=None)
    imr_nm_ris = models.TextField(null=True,blank=True,default=None)
    ipm_nm = models.TextField(null=True,blank=True,default=None)
    ipm_nm_ris = models.TextField(null=True,blank=True,default=None)
    kan_nm = models.TextField(null=True,blank=True,default=None)
    kan_nm_ris = models.TextField(null=True,blank=True,default=None)
    lnz_nm = models.TextField(null=True,blank=True,default=None)
    lnz_nm_ris = models.TextField(null=True,blank=True,default=None)
    lvx_nm = models.TextField(null=True,blank=True,default=None)
    lvx_nm_ris = models.TextField(null=True,blank=True,default=None)
    man_nm = models.TextField(null=True,blank=True,default=None)
    man_nm_ris = models.TextField(null=True,blank=True,default=None)
    mem_nm = models.TextField(null=True,blank=True,default=None)
    mem_nm_ris = models.TextField(null=True,blank=True,default=None)
    mev_nm = models.TextField(null=True,blank=True,default=None)
    mev_nm_ris = models.TextField(null=True,blank=True,default=None)
    mfx_nm = models.TextField(null=True,blank=True,default=None)
    mfx_nm_ris = models.TextField(null=True,blank=True,default=None)
    mno_nm = models.TextField(null=True,blank=True,default=None)
    mno_nm_ris = models.TextField(null=True,blank=True,default=None)
    nal_nm = models.TextField(null=True,blank=True,default=None)
    nal_nm_ris = models.TextField(null=True,blank=True,default=None)
    net_nm = models.TextField(null=True,blank=True,default=None)
    net_nm_ris = models.TextField(null=True,blank=True,default=None)
    nit_nm = models.TextField(null=True,blank=True,default=None)
    nit_nm_ris = models.TextField(null=True,blank=True,default=None)
    nor_nm = models.TextField(null=True,blank=True,default=None)
    nor_nm_ris = models.TextField(null=True,blank=True,default=None)
    nov_nm = models.TextField(null=True,blank=True,default=None)
    nov_nm_ris = models.TextField(null=True,blank=True,default=None)
    ofx_nm = models.TextField(null=True,blank=True,default=None)
    ofx_nm_ris = models.TextField(null=True,blank=True,default=None)
    oxa_nm = models.TextField(null=True,blank=True,default=None)
    oxa_nm_ris = models.TextField(null=True,blank=True,default=None)
    pen_nm = models.TextField(null=True,blank=True,default=None)
    pen_nm_ris = models.TextField(null=True,blank=True,default=None)
    pip_nm = models.TextField(null=True,blank=True,default=None)
    pip_nm_ris = models.TextField(null=True,blank=True,default=None)
    plz_nm = models.TextField(null=True,blank=True,default=None)
    plz_nm_ris = models.TextField(null=True,blank=True,default=None)
    pol_nm = models.TextField(null=True,blank=True,default=None)
    pol_nm_ris = models.TextField(null=True,blank=True,default=None)
    qda_nm = models.TextField(null=True,blank=True,default=None)
    qda_nm_ris = models.TextField(null=True,blank=True,default=None)
    rif_nm = models.TextField(null=True,blank=True,default=None)
    rif_nm_ris = models.TextField(null=True,blank=True,default=None)
    sam_nm = models.TextField(null=True,blank=True,default=None)
    sam_nm_ris = models.TextField(null=True,blank=True,default=None)
    spt_nm = models.TextField(null=True,blank=True,default=None)
    spt_nm_ris = models.TextField(null=True,blank=True,default=None)
    sss_nm = models.TextField(null=True,blank=True,default=None)
    sss_nm_ris = models.TextField(null=True,blank=True,default=None)
    sth_nm = models.TextField(null=True,blank=True,default=None)
    sth_nm_ris = models.TextField(null=True,blank=True,default=None)
    str_nm = models.TextField(null=True,blank=True,default=None)
    str_nm_ris = models.TextField(null=True,blank=True,default=None)
    sxt_nm = models.TextField(null=True,blank=True,default=None)
    sxt_nm_ris = models.TextField(null=True,blank=True,default=None)
    tcc_nm = models.TextField(null=True,blank=True,default=None)
    tcc_nm_ris = models.TextField(null=True,blank=True,default=None)
    tcy_nm = models.TextField(null=True,blank=True,default=None)
    tcy_nm_ris = models.TextField(null=True,blank=True,default=None)
    tgc_nm = models.TextField(null=True,blank=True,default=None)
    tgc_nm_ris = models.TextField(null=True,blank=True,default=None)
    tic_nm = models.TextField(null=True,blank=True,default=None)
    tic_nm_ris = models.TextField(null=True,blank=True,default=None)
    tob_nm = models.TextField(null=True,blank=True,default=None)
    tob_nm_ris = models.TextField(null=True,blank=True,default=None)
    tzd_nm = models.TextField(null=True,blank=True,default=None)
    tzd_nm_ris = models.TextField(null=True,blank=True,default=None)
    tzp_nm = models.TextField(null=True,blank=True,default=None)
    tzp_nm_ris = models.TextField(null=True,blank=True,default=None)
    van_nm = models.TextField(null=True,blank=True,default=None)
    van_nm_ris = models.TextField(null=True,blank=True,default=None)

    amb_nm = models.TextField(null=True,blank=True,default=None)
    amb_nm_ris = models.TextField(null=True,blank=True,default=None)
    cpt_nm = models.TextField(null=True,blank=True,default=None)
    cpt_nm_ris = models.TextField(null=True,blank=True,default=None)
    fct_nm = models.TextField(null=True,blank=True,default=None)
    fct_nm_ris = models.TextField(null=True,blank=True,default=None)
    pri_nm = models.TextField(null=True,blank=True,default=None)
    pri_nm_ris = models.TextField(null=True,blank=True,default=None)
    spx_nm = models.TextField(null=True,blank=True,default=None)
    spx_nm_ris = models.TextField(null=True,blank=True,default=None)
    tec_nm = models.TextField(null=True,blank=True,default=None)
    tec_nm_ris = models.TextField(null=True,blank=True,default=None)
    tlt_nm = models.TextField(null=True,blank=True,default=None)
    tlt_nm_ris = models.TextField(null=True,blank=True,default=None)

    
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.referred
    

# class Process(models.Model):
#     batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
#     process = models.TextField(null=True,blank=True,default=None)
#     start_date = models.DateField(null=True,blank=True,default=None)
#     start_sign = models.TextField(null=True,blank=True,default=None)
#     finish_date = models.DateField(null=True,blank=True,default=None)
#     finish_sign = models.TextField(null=True,blank=True,default=None)
#     remarks = models.TextField(null=True,blank=True,default=None)
#     running_tat = models.TextField(null=True,blank=True,default=None)
#     days_completed = models.TextField(null=True,blank=True,default=None)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.process
    
#     def get_format_date_start(self):
#         if self.start_date != None:
#             date_received = datetime.datetime.strftime(self.start_date, '%m/%d/%Y')
#         else:
#             date_received = None
#         return date_received
    
#     def finish_date_format(self):
#         if self.finish_date != None:
#             date_received = datetime.datetime.strftime(self.finish_date, '%m/%d/%Y')
#         else:
#             date_received = None
#         return date_received

    
#     def get_running_tat(self):
#         batch = Batches.objects.get(id=self.batch_id)
#         holidays = Holiday.objects.all().values_list('holiday',flat=True)
#         diff = np.busday_count( batch.date_received,self.finish_date,holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
#         return diff
    

