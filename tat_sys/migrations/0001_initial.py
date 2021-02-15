# Generated by Django 3.0.3 on 2021-02-01 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.TextField(blank=True, default=None, null=True, unique=True)),
                ('site', models.TextField(max_length=3)),
                ('accession_number', models.TextField(max_length=99)),
                ('isolate_number', models.IntegerField()),
                ('total_isolate_number', models.IntegerField()),
                ('batch_number', models.IntegerField()),
                ('total_batch_number', models.IntegerField()),
                ('date_received', models.DateField()),
                ('received_by', models.TextField(max_length=99)),
                ('status', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.TextField(blank=True, default=None, null=True)),
                ('start_date', models.DateField(blank=True, default=None, null=True)),
                ('start_sign', models.TextField(blank=True, default=None, null=True)),
                ('finish_date', models.DateField(blank=True, default=None, null=True)),
                ('finish_sign', models.TextField(blank=True, default=None, null=True)),
                ('remarks', models.TextField(blank=True, default=None, null=True)),
                ('running_tat', models.TextField(blank=True, default=None, null=True)),
                ('days_completed', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Batches')),
            ],
        ),
    ]