# Generated by Django 4.1 on 2024-04-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tat_sys", "0004_rename_amc_disk_historicalsitediskresult_amc_nd20_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="arsrldiskresult",
            name="amb_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="amb_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="cpt_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="cpt_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="fct_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="fct_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="pri_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="pri_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="tec_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="tec_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="tlt_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrldiskresult",
            name="tlt_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="amb_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="amb_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="cpt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="cpt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="fct_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="fct_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="pri_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="pri_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="tec_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="tec_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="tlt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="arsrlmicresult",
            name="tlt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="amb_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="amb_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="cpt_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="cpt_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="fct_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="fct_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="pri_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="pri_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="tec_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="tec_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="tlt_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrldiskresult",
            name="tlt_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="amb_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="amb_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="cpt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="cpt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="fct_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="fct_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="pri_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="pri_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="tec_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="tec_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="tlt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalarsrlmicresult",
            name="tlt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="amb_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="amb_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="cpt_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="cpt_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="fct_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="fct_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="pri_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="pri_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="tec_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="tec_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="tlt_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitediskresult",
            name="tlt_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="amb_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="amb_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="cpt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="cpt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="fct_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="fct_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="pri_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="pri_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="tec_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="tec_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="tlt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalsitemicresult",
            name="tlt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="amb_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="amb_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="cpt_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="cpt_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="fct_nd10",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="fct_nd10_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="pri_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="pri_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="tec_nd30",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="tec_nd30_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="tlt_nd15",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitediskresult",
            name="tlt_nd15_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="amb_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="amb_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="cpt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="cpt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="fct_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="fct_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="pri_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="pri_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="spx_nd5",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="spx_nd5_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="tec_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="tec_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="tlt_nm",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="sitemicresult",
            name="tlt_nm_ris",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
