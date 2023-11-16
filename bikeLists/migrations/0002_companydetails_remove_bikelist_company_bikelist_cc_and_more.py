# Generated by Django 4.2.4 on 2023-09-03 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bikeLists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=50)),
                ("origin", models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name="bikelist",
            name="company",
        ),
        migrations.AddField(
            model_name="bikelist",
            name="cc",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bikelist",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="bikelist",
            name="company_details",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bikelist",
                to="bikeLists.companydetails",
            ),
            preserve_default=False,
        ),
    ]
