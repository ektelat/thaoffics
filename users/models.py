from io import BytesIO

from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os

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
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        if not phone_number:
            raise ValueError('The phone number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    name = models.TextField(blank=True)
    id_number=models.TextField(blank=True)
    address=models.TextField(blank=True)
    phone_number = models.CharField(unique=True, blank=True ,max_length=20)
    profile_pic = models.ImageField(blank=True,upload_to='user_profiles')
    bio = models.TextField(blank=True)
    is_phone_verified=models.BooleanField(blank=False,default=False)
    is_email_verified=models.BooleanField(blank=False,default=False)
    is_active=models.BooleanField(default=True,blank=False)
    country_code=models.CharField(blank=True,max_length=5)
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()


    # Define the groups and permissions for the user model
    class Groups:
        OWNER = 'Owner'
        STAFF = 'Staff'
        CUSTOMER = 'Customer'

    def save(self, *args, **kwargs):
        if self.id:
            try:
                old_user = User.objects.get(pk=self.id)
                if old_user.profile_pic != self.profile_pic:
                    if old_user.profile_pic:
                        # Delete the old profile picture
                        old_user.profile_pic.delete(save=False)
            except User.DoesNotExist:
                pass

        # Set the profile_pic filename as the user id
        if self.profile_pic:
            ext = os.path.splitext(self.profile_pic.name)[1].lower()
            self.profile_pic.name = f'user_profiles/{self.id}{ext}'

        # Override the save() method to resize the image and save it as PNG
        super().save(*args, **kwargs)

        if self.profile_pic:
            img = Image.open(default_storage.open(self.profile_pic.name))
            img = img.convert('RGB')
            img.thumbnail((500, 500))

            # Save the image to a BytesIO buffer
            image_buffer = BytesIO()
            img.save(image_buffer, format='PNG', quality=90)
            image_buffer.seek(0)

            # Save the image to the storage backend
            default_storage.save(self.profile_pic.name, image_buffer)

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