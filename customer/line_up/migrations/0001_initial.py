# Generated by Django 2.2.11 on 2020-03-30 05:05

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phone_field.models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=5)),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_phone_number', phone_field.models.PhoneField(max_length=31)),
                ('timezone', timezone_field.fields.TimeZoneField(choices=[('America/New_York', 'America/New_York'), ('America/Detroit', 'America/Detroit'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('America/Chicago', 'America/Chicago'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('America/Menominee', 'America/Menominee'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('America/Denver', 'America/Denver'), ('America/Boise', 'America/Boise'), ('America/Phoenix', 'America/Phoenix'), ('America/Los_Angeles', 'America/Los_Angeles'), ('America/Anchorage', 'America/Anchorage'), ('America/Juneau', 'America/Juneau'), ('America/Sitka', 'America/Sitka'), ('America/Metlakatla', 'America/Metlakatla'), ('America/Yakutat', 'America/Yakutat'), ('America/Nome', 'America/Nome'), ('America/Adak', 'America/Adak'), ('Pacific/Honolulu', 'Pacific/Honolulu')])),
                ('business_open', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('phone_number', phone_field.models.PhoneField(max_length=31)),
                ('up_next_text_sent', models.BooleanField(default=False)),
                ('entered_store', models.BooleanField(default=False)),
                ('no_show', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
                ('time_up', models.BooleanField(default=False)),
                ('image', models.CharField(blank=True, max_length=500, null=True)),
                ('store_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_up.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_up.Store')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
