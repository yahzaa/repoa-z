# Generated by Django 2.1.1 on 2018-09-26 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college_api', '0005_auto_20180926_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='college_api.Team'),
        ),
    ]
