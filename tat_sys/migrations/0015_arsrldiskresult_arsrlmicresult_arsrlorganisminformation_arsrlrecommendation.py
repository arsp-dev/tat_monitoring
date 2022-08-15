# Generated by Django 3.0.3 on 2022-06-15 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tat_sys', '0014_remove_sitemicresult_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArsrlRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation_code', models.TextField(blank=True, default=None, null=True)),
                ('recommendation', models.TextField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('created_by', models.TextField(blank=True, default=None, null=True)),
                ('updated_by', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Referred')),
            ],
        ),
        migrations.CreateModel(
            name='ArsrlOrganismInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ampc', models.TextField(blank=True, default=None, null=True)),
                ('esbl', models.TextField(blank=True, default=None, null=True)),
                ('carb', models.TextField(blank=True, default=None, null=True)),
                ('ecim', models.TextField(blank=True, default=None, null=True)),
                ('mcim', models.TextField(blank=True, default=None, null=True)),
                ('ec_mcim', models.TextField(blank=True, default=None, null=True)),
                ('mbl', models.TextField(blank=True, default=None, null=True)),
                ('bl', models.TextField(blank=True, default=None, null=True)),
                ('mr', models.TextField(blank=True, default=None, null=True)),
                ('meca', models.TextField(blank=True, default=None, null=True)),
                ('icr', models.TextField(blank=True, default=None, null=True)),
                ('arsl_pre', models.TextField(blank=True, default=None, null=True)),
                ('org_code', models.TextField(blank=True, default=None, null=True)),
                ('org_name', models.TextField(blank=True, default=None, null=True)),
                ('arsrl_post', models.TextField(blank=True, default=None, null=True)),
                ('created_by', models.TextField(blank=True, default=None, null=True)),
                ('updated_by', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Referred')),
            ],
        ),
        migrations.CreateModel(
            name='ArsrlMicResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amk_mic', models.TextField(blank=True, default=None, null=True)),
                ('amk_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('amc_mic', models.TextField(blank=True, default=None, null=True)),
                ('amc_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('amp_mic', models.TextField(blank=True, default=None, null=True)),
                ('amp_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('sam_mic', models.TextField(blank=True, default=None, null=True)),
                ('sam_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('atm_mic', models.TextField(blank=True, default=None, null=True)),
                ('atm_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('azm_mic', models.TextField(blank=True, default=None, null=True)),
                ('azm_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cec_mic', models.TextField(blank=True, default=None, null=True)),
                ('cec_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('man_mic', models.TextField(blank=True, default=None, null=True)),
                ('man_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('czo_mic', models.TextField(blank=True, default=None, null=True)),
                ('czo_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('fep_mic', models.TextField(blank=True, default=None, null=True)),
                ('fep_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cfm_mic', models.TextField(blank=True, default=None, null=True)),
                ('cfm_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cfp_mic', models.TextField(blank=True, default=None, null=True)),
                ('cfp_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('ctx_mic', models.TextField(blank=True, default=None, null=True)),
                ('ctx_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('fox_mic', models.TextField(blank=True, default=None, null=True)),
                ('fox_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('caz_mic', models.TextField(blank=True, default=None, null=True)),
                ('caz_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cro_mic', models.TextField(blank=True, default=None, null=True)),
                ('cro_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cxa_mic', models.TextField(blank=True, default=None, null=True)),
                ('cxa_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cep_mic', models.TextField(blank=True, default=None, null=True)),
                ('cep_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('chl_mic', models.TextField(blank=True, default=None, null=True)),
                ('chl_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cip_mic', models.TextField(blank=True, default=None, null=True)),
                ('cip_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('clr_mic', models.TextField(blank=True, default=None, null=True)),
                ('clr_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('cli_mic', models.TextField(blank=True, default=None, null=True)),
                ('cli_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('sxt_mic', models.TextField(blank=True, default=None, null=True)),
                ('sxt_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('ery_mic', models.TextField(blank=True, default=None, null=True)),
                ('ery_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('gen_mic', models.TextField(blank=True, default=None, null=True)),
                ('gen_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('ipm_mic', models.TextField(blank=True, default=None, null=True)),
                ('ipm_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('kan_mic', models.TextField(blank=True, default=None, null=True)),
                ('kan_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('lev_mic', models.TextField(blank=True, default=None, null=True)),
                ('lev_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('nal_mic', models.TextField(blank=True, default=None, null=True)),
                ('nal_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('net_mic', models.TextField(blank=True, default=None, null=True)),
                ('net_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('nit_mic', models.TextField(blank=True, default=None, null=True)),
                ('nit_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('nor_mic', models.TextField(blank=True, default=None, null=True)),
                ('nor_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('ofx_mic', models.TextField(blank=True, default=None, null=True)),
                ('ofx_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('oxa_mic', models.TextField(blank=True, default=None, null=True)),
                ('oxa_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('pen_mic', models.TextField(blank=True, default=None, null=True)),
                ('pen_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('pip_mic', models.TextField(blank=True, default=None, null=True)),
                ('pip_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('rif_mic', models.TextField(blank=True, default=None, null=True)),
                ('rif_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('spe_mic', models.TextField(blank=True, default=None, null=True)),
                ('spe_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('str_mic', models.TextField(blank=True, default=None, null=True)),
                ('str_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tet_mic', models.TextField(blank=True, default=None, null=True)),
                ('tet_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tic_mic', models.TextField(blank=True, default=None, null=True)),
                ('tic_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tcc_mic', models.TextField(blank=True, default=None, null=True)),
                ('tcc_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tob_mic', models.TextField(blank=True, default=None, null=True)),
                ('tob_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('van_mic', models.TextField(blank=True, default=None, null=True)),
                ('van_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('mfx_mic', models.TextField(blank=True, default=None, null=True)),
                ('mfx_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('mem_mic', models.TextField(blank=True, default=None, null=True)),
                ('mem_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tzp_mic', models.TextField(blank=True, default=None, null=True)),
                ('tzp_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('geh_mic', models.TextField(blank=True, default=None, null=True)),
                ('geh_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('sth_mic', models.TextField(blank=True, default=None, null=True)),
                ('sth_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('lnz_mic', models.TextField(blank=True, default=None, null=True)),
                ('lnz_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('nov_mic', models.TextField(blank=True, default=None, null=True)),
                ('nov_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('etp_mic', models.TextField(blank=True, default=None, null=True)),
                ('etp_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('dor_mic', models.TextField(blank=True, default=None, null=True)),
                ('dor_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('tgc_mic', models.TextField(blank=True, default=None, null=True)),
                ('tgc_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('col_mic', models.TextField(blank=True, default=None, null=True)),
                ('col_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('pol_mic', models.TextField(blank=True, default=None, null=True)),
                ('pol_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('dox_mic', models.TextField(blank=True, default=None, null=True)),
                ('dox_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('qda_mic', models.TextField(blank=True, default=None, null=True)),
                ('qda_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('mno_mic', models.TextField(blank=True, default=None, null=True)),
                ('mno_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('dap_mic', models.TextField(blank=True, default=None, null=True)),
                ('dap_mic_ris', models.TextField(blank=True, default=None, null=True)),
                ('created_by', models.TextField(blank=True, default=None, null=True)),
                ('updated_by', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Referred')),
            ],
        ),
        migrations.CreateModel(
            name='ArsrlDiskResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amk_disk', models.TextField(blank=True, default=None, null=True)),
                ('amk_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('amc_disk', models.TextField(blank=True, default=None, null=True)),
                ('amc_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('amp_disk', models.TextField(blank=True, default=None, null=True)),
                ('amp_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('sam_disk', models.TextField(blank=True, default=None, null=True)),
                ('sam_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('atm_disk', models.TextField(blank=True, default=None, null=True)),
                ('atm_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('azm_disk', models.TextField(blank=True, default=None, null=True)),
                ('azm_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cec_disk', models.TextField(blank=True, default=None, null=True)),
                ('cec_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('man_disk', models.TextField(blank=True, default=None, null=True)),
                ('man_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('czo_disk', models.TextField(blank=True, default=None, null=True)),
                ('czo_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('fep_disk', models.TextField(blank=True, default=None, null=True)),
                ('fep_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cfm_disk', models.TextField(blank=True, default=None, null=True)),
                ('cfm_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cfp_disk', models.TextField(blank=True, default=None, null=True)),
                ('cfp_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('ctx_disk', models.TextField(blank=True, default=None, null=True)),
                ('ctx_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('fox_disk', models.TextField(blank=True, default=None, null=True)),
                ('fox_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('caz_disk', models.TextField(blank=True, default=None, null=True)),
                ('caz_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cro_disk', models.TextField(blank=True, default=None, null=True)),
                ('cro_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cxa_disk', models.TextField(blank=True, default=None, null=True)),
                ('cxa_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cep_disk', models.TextField(blank=True, default=None, null=True)),
                ('cep_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('chl_disk', models.TextField(blank=True, default=None, null=True)),
                ('chl_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cip_disk', models.TextField(blank=True, default=None, null=True)),
                ('cip_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('clr_disk', models.TextField(blank=True, default=None, null=True)),
                ('clr_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('cli_disk', models.TextField(blank=True, default=None, null=True)),
                ('cli_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('sxt_disk', models.TextField(blank=True, default=None, null=True)),
                ('sxt_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('ery_disk', models.TextField(blank=True, default=None, null=True)),
                ('ery_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('gen_disk', models.TextField(blank=True, default=None, null=True)),
                ('gen_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('ipm_disk', models.TextField(blank=True, default=None, null=True)),
                ('ipm_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('kan_disk', models.TextField(blank=True, default=None, null=True)),
                ('kan_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('lev_disk', models.TextField(blank=True, default=None, null=True)),
                ('lev_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('nal_disk', models.TextField(blank=True, default=None, null=True)),
                ('nal_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('net_disk', models.TextField(blank=True, default=None, null=True)),
                ('net_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('nit_disk', models.TextField(blank=True, default=None, null=True)),
                ('nit_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('nor_disk', models.TextField(blank=True, default=None, null=True)),
                ('nor_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('ofx_disk', models.TextField(blank=True, default=None, null=True)),
                ('ofx_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('oxa_disk', models.TextField(blank=True, default=None, null=True)),
                ('oxa_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('pen_disk', models.TextField(blank=True, default=None, null=True)),
                ('pen_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('pip_disk', models.TextField(blank=True, default=None, null=True)),
                ('pip_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('rif_disk', models.TextField(blank=True, default=None, null=True)),
                ('rif_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('spe_disk', models.TextField(blank=True, default=None, null=True)),
                ('spe_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('str_disk', models.TextField(blank=True, default=None, null=True)),
                ('str_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tet_disk', models.TextField(blank=True, default=None, null=True)),
                ('tet_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tic_disk', models.TextField(blank=True, default=None, null=True)),
                ('tic_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tcc_disk', models.TextField(blank=True, default=None, null=True)),
                ('tcc_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tob_disk', models.TextField(blank=True, default=None, null=True)),
                ('tob_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('van_disk', models.TextField(blank=True, default=None, null=True)),
                ('van_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('mfx_disk', models.TextField(blank=True, default=None, null=True)),
                ('mfx_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('mem_disk', models.TextField(blank=True, default=None, null=True)),
                ('mem_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tzp_disk', models.TextField(blank=True, default=None, null=True)),
                ('tzp_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('geh_disk', models.TextField(blank=True, default=None, null=True)),
                ('geh_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('sth_disk', models.TextField(blank=True, default=None, null=True)),
                ('sth_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('lnz_disk', models.TextField(blank=True, default=None, null=True)),
                ('lnz_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('nov_disk', models.TextField(blank=True, default=None, null=True)),
                ('nov_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('etp_disk', models.TextField(blank=True, default=None, null=True)),
                ('etp_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('dor_disk', models.TextField(blank=True, default=None, null=True)),
                ('dor_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('tgc_disk', models.TextField(blank=True, default=None, null=True)),
                ('tgc_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('col_disk', models.TextField(blank=True, default=None, null=True)),
                ('col_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('pol_disk', models.TextField(blank=True, default=None, null=True)),
                ('pol_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('dox_disk', models.TextField(blank=True, default=None, null=True)),
                ('dox_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('qda_disk', models.TextField(blank=True, default=None, null=True)),
                ('qda_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('mno_disk', models.TextField(blank=True, default=None, null=True)),
                ('mno_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('dap_disk', models.TextField(blank=True, default=None, null=True)),
                ('dap_disk_ris', models.TextField(blank=True, default=None, null=True)),
                ('comments', models.TextField(blank=True, default=None, null=True)),
                ('created_by', models.TextField(blank=True, default=None, null=True)),
                ('updated_by', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tat_sys.Referred')),
            ],
        ),
    ]
