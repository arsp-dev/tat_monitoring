from django.db import models
import pandas as pd
import numpy as np
import datetime
from django.forms import model_to_dict


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
    site = models.TextField(max_length=3)
    accession_number = models.TextField(max_length=99)
    isolate_number = models.IntegerField()
    total_isolate_number = models.IntegerField()
    batch_number = models.IntegerField()
    total_batch_number = models.IntegerField()
    date_received = models.DateField()
    received_by = models.TextField(max_length=99)
    status = models.TextField(null=True,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_current_status(self):
        p = Process.objects.filter(batch_id=self.id).last()
        ret = p.process
        
        if '1_' in ret:
            ret = 'Processing'
        elif '2_' in ret:
            ret = 'Encoding'
        elif '3_' in ret:
            ret = 'Editing'
        elif '4_' in ret:
            ret = 'Lab Verification'
        elif '5_' in ret:
            ret = 'Final Verification'
        elif '6_' in ret:
            ret = 'Releasing'
            
        return ret
    get_current_status = property(get_current_status)
    
  

    def __str__(self):
        return self.batch_name
    
    def get_running_tat(self):
        holidays = Holiday.objects.all().values_list('holiday',flat=True)
        diff = np.busday_count( self.date_received,datetime.date.today(),holidays=holidays,weekmask=[1,1,1,1,1,1,0] )
        return diff
    
    
    def get_absolute_url(self):
        return "batches/%i/" % self.id
    
    
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