from django.db import models
from django.contrib.auth.models import AbstractUser
class ExcelFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User
import random

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp_code = otp
        self.save()
        return otp


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.timestamp}"



# models.py

from django.db import models

class ParticipantConsent(models.Model):
    unique_id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    
    respiratory_conditions = models.CharField(max_length=255, blank=True, null=True)
    cardiovascular_conditions = models.CharField(max_length=255, blank=True, null=True)
    cardiovascular_symptoms = models.CharField(max_length=255, blank=True, null=True)
    metabolic_conditions = models.CharField(max_length=255, blank=True, null=True)
    mental_health_conditions = models.CharField(max_length=255, blank=True, null=True)
    stress_level = models.CharField(max_length=50)
    
    lifestyle_factors = models.CharField(max_length=255, blank=True, null=True)
    sleep_hours = models.CharField(max_length=50)
    sleep_disorders = models.CharField(max_length=255, blank=True, null=True)
    
    last_medical_checkup = models.CharField(max_length=50)
    health_concerns = models.CharField(max_length=255, blank=True, null=True)

    date_submitted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Participant {self.unique_id}"
        
from django.db import models
from django.contrib.auth.models import User  # Import User model

from django.db import models
from django.contrib.auth.models import User

class GoogleSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    sheet_url = models.URLField()
    title = models.CharField(max_length=255,default='NONE')  # New title attribute
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.sheet_url}"


# models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"







from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    form_submitted = models.BooleanField(default=False)












from django.db import models

# Create your models here.
from django.db import models


from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)

class File(models.Model):
    name = models.CharField(max_length=255)
    file_url = models.URLField()  # or FileField/ImageField depending on your need
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
# papers/models.py

from django.db import models

class FileModel(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')  # Adjust according to your needs

    def __str__(self):
        return self.name

# models.py
from django.db import models

from django.db import models

class VisitorCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    @classmethod
    def increment(cls):
        # Use the first record, or create a new one if it doesn't exist
        visitor_count, created = cls.objects.get_or_create(id=1)  # Assuming only one row for visitor count
        visitor_count.count += 1
        visitor_count.save()
        return visitor_count.count

    def __str__(self):
        return f"Total Visitors: {self.count}"


class CustomUser(AbstractUser):
    is_visitor_counted = models.BooleanField(default=False)

    # Add related_name to resolve the reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Adjust the related_name here
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Adjust the related_name here
        blank=True
    )

    def __str__(self):
        return self.username
