# Generated by Django 4.2.16 on 2024-09-30 10:09

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
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=50)),
                ('template_heading', models.CharField(max_length=100)),
                ('template_body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User_registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('mobile_num', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='User_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'admin'), ('customer', 'customer')], max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('contact_no', models.BigIntegerField()),
                ('user_status', models.CharField(blank=True, max_length=50)),
                ('company', models.CharField(blank=True, max_length=30)),
                ('business_email', models.EmailField(max_length=254)),
                ('years_of_experience', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('job_position', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('otp', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('course_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(max_length=150)),
                ('follow_up', models.CharField(max_length=50)),
                ('time', models.TimeField(blank=True, null=True)),
                ('sent_status', models.BooleanField(default=False)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement_app.template')),
                ('users', models.ManyToManyField(to='usermanagement_app.user_details')),
            ],
        ),
    ]