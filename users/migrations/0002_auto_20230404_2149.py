from django.db import migrations
from django.contrib.auth.models import Group, Permission
from users.models import User, Permissions
from django.contrib.contenttypes.models import ContentType


def create_groups_and_permissions(apps, schema_editor):
    permission_names = [
        Permissions.CREATE_COMPANY,
        Permissions.SET_STORAGE_PLAN,
        Permissions.ADD_STAFF_BY_EMAIL,
        Permissions.VIEW_EMPLOYEES,
        Permissions.SEND_TASKS,
        Permissions.SEND_MESSAGES,
        Permissions.SUBSCRIBE,
        Permissions.CONTACT_OFFICE,
        Permissions.SEND_MESSAGES_TO_OFFICE,
    ]
    for pr in permission_names:
        print(pr)
        content_type = ContentType.objects.get_for_model(apps.get_model('users', 'User'))
        permission = Permission.objects.create(
            content_type=content_type,
            codename=pr[0],
            name=pr[1]
        )
        print(permission)



    # Create owner group and permissions
    owner_group = Group.objects.create(name=User.Groups.OWNER)
    owner_group.permissions.add(*Permission.objects.filter(codename__in=[
        Permissions.CREATE_COMPANY[0],
        Permissions.SET_STORAGE_PLAN[0],
        Permissions.ADD_STAFF_BY_EMAIL[0],
    ]))

    # Create staff group and permissions
    staff_group = Group.objects.create(name=User.Groups.STAFF)
    staff_group.permissions.add(*Permission.objects.filter(codename__in=[
        Permissions.VIEW_EMPLOYEES[0],
        Permissions.SEND_TASKS[0],
        Permissions.SEND_MESSAGES[0],
    ]))

    # Create customer group and permissions
    customer_group = Group.objects.create(name=User.Groups.CUSTOMER)
    customer_group.permissions.add(*Permission.objects.filter(codename__in=[
        Permissions.SUBSCRIBE[0],
        Permissions.CONTACT_OFFICE[0],
        Permissions.SEND_MESSAGES_TO_OFFICE[0],
    ]))

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
