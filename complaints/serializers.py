from rest_framework import serializers
from .models import Complaint, ComplaintImage

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'description', 'latitude', 'longitude', 'status']
        read_only_fields = ['status']  
class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image']