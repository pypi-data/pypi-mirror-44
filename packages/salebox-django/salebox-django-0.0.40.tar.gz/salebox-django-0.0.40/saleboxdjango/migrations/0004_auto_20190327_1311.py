# Generated by Django 2.1.4 on 2019-03-27 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saleboxdjango', '0003_member_salebox_member_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutstore',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
