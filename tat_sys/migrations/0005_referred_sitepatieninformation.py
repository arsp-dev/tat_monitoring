# Generated by Django 3.0.3 on 2022-06-08 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tat_sys', '0004_auto_20220608_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.TextField(blank=True, default=None, null=True)),
                ('lab_number', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.TextField(blank=True, default='<django.db.models.query_utils.DeferredAttribute object at 0x03F79330> <django.db.models.query_utils.DeferredAttribute object at 0x03F79350>', null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Batches')),
            ],
        ),
        migrations.CreateModel(
            name='SitePatienInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_number', models.TextField(blank=True, default=None, null=True)),
                ('date_of_birth', models.DateField()),
                ('first_name', models.TextField(blank=True, default=None, null=True)),
                ('middle_name', models.TextField(blank=True, default=None, null=True)),
                ('last_name', models.TextField(blank=True, default=None, null=True)),
                ('sex', models.TextField(blank=True, default=None, null=True)),
                ('date_of_admission', models.DateField()),
                ('nosocomial', models.TextField(blank=True, default=None, null=True)),
                ('diagnosis', models.TextField(blank=True, default=None, null=True)),
                ('icd_10_code', models.TextField(blank=True, default=None, null=True)),
                ('ward', models.TextField(blank=True, default=None, null=True)),
                ('service_type', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Referred')),
            ],
        ),
    ]
