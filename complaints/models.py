from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('new', 'قيد الانتظار'),
        ('in_progress', 'قيد المعالجة'),
        ('resolved', 'محلولة'),
        ('rejected','مرفوض')
    ]

    COMPLAINT_TYPE_CHOICES = [
        ('lighting', 'إنارة'),
        ('road', 'طرق'),
        ('garbage', 'نفايات'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
      if self.user:
         return f"{self.user.username} - {self.complaint_type}"
      
class ComplaintImage(models.Model):

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='complaints/%Y/%m/%d'
    )

    def __str__(self):
        return f"Image for {self.complaint.id}"  
    