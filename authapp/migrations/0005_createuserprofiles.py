# Generated by Django 2.2.13 on 2020-06-11 11:40

from django.db import migrations, transaction


def forwards_func(apps, schema_editor):
    HoHooUser = apps.get_model('authapp', 'HoHooUser')
    UserProfile = apps.get_model('authapp', 'UserProfile')
    with transaction.atomic():
        for user in HoHooUser.objects.all():
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)


def reverse_func(apps, schema_editor):
    UserProfile = apps.get_model('authapp', 'UserProfile')
    with transaction.atomic():
        UserProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_userprofile'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]