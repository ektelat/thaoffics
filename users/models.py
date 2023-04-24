from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group


class Permissions:
    # Owner permissions
    CREATE_COMPANY = ('create_company', 'Can create a new company')
    SET_STORAGE_PLAN = ('set_storage_plan', 'Can set storage plan for the company')
    ADD_STAFF_BY_EMAIL = ('add_staff_by_email', 'Can add staff by email')

    # Staff permissions
    VIEW_EMPLOYEES = ('view_employees', 'Can view all employees')
    SEND_TASKS = ('send_tasks', 'Can send tasks to all employees or customers')
    SEND_MESSAGES = ('send_messages', 'Can send messages to all employees or customers')

    # Customer permissions
    SUBSCRIBE = ('subscribe', 'Can subscribe to the service')
    CONTACT_OFFICE = ('contact_office', 'Can contact the office through a special number')
    SEND_MESSAGES_TO_OFFICE = ('send_messages_to_office', 'Can send and receive messages from the office with files or pictures')


class User(AbstractUser):
    name = models.TextField(blank=True)
    id_number=models.TextField(blank=True)
    address=models.TextField(blank=True)
    phone_number = models.CharField(unique=True, blank=True ,max_length=20)
    profile_pic = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    is_phone_verified=models.BooleanField(blank=False,default=False)
    is_email_verified=models.BooleanField(blank=False,default=False)
    is_active=models.BooleanField(default=True,blank=False)
    country_code=models.CharField(blank=True,max_length=5)
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "phone_number"


    # Define the groups and permissions for the user model
    class Groups:
        OWNER = 'Owner'
        STAFF = 'Staff'
        CUSTOMER = 'Customer'
        

    def __str__(self):
        return self.phone_number

    def is_owner(self):
        return self.groups.filter(name=User.Groups.OWNER).exists()

    def is_staff(self):
        return self.groups.filter(name=User.Groups.STAFF).exists()

    def is_customer(self):
        return self.groups.filter(name=User.Groups.CUSTOMER).exists()


from django.utils import timezone

class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
