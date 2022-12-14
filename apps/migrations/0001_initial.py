# Generated by Django 4.1 on 2022-09-03 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='tadbirModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nametadbir', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('closeEvent', models.BooleanField(default=False)),
                ('authuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ratsiyaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('katalog', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('qr_code', models.CharField(max_length=200)),
                ('lasteventid', models.PositiveIntegerField(default=0)),
                ('archive', models.BooleanField(default=False)),
                ('tadbir', models.ManyToManyField(through='apps.Enrollment', to='apps.tadbirmodel')),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='ratsiyaModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.ratsiyamodel'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='tadbirModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.tadbirmodel'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('tadbirModel', 'ratsiyaModel')},
        ),
    ]
