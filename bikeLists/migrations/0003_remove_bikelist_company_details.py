# Generated by Django 4.2.4 on 2023-09-13 15:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "bikeLists",
            "0002_companydetails_remove_bikelist_company_bikelist_cc_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bikelist",
            name="company_details",
        ),
    ]