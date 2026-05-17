from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Complaint, ComplaintImage
from .serializers import ComplaintSerializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

class ComplaintCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user)

        images = request.FILES.getlist('images')

        # 1️⃣ التحقق من الصور أولاً
        if len(images) < 1:
            return Response(
                {"error": "يجب رفع صورة واحدة على الأقل"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(images) > 5:
            return Response(
                {"error": "الحد الأقصى 5 صور"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ إنشاء البلاغ
        serializer = ComplaintSerializer(data=request.data)
        

        if serializer.is_valid():
            mapping = {
                'lighting': 'electricity',
                'road': 'roads',
                'garbage': 'sanitation'
            }

            assigned_to = mapping.get(request.data.get('complaint_type'))

            complaint = serializer.save(
               user=request.user,
               assigned_to=assigned_to
            )

            # 3️⃣ حفظ الصور
            for img in images:
                ComplaintImage.objects.create(
                    complaint=complaint,
                    image=img
                )

            data = ComplaintSerializer(complaint).data
            data["assigned_to"] = assigned_to
            
            return Response(data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def add_complaint_view(request):
    return render(request, 'complaints/add_complaint.html')

#@login_required
#def track_complaints_view(request):

    # جلب بلاغات المستخدم الحالي
    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'complaints/track.html', {
        'complaints': complaints
    })
def track_complaints_view(request):
    return render(request, 'complaints/track.html')

class MyComplaintsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')

        data = []
        for c in complaints:
            data.append({
                "id": c.id,
                "complaint_type": c.complaint_type,
                "description": c.description,
                "status": c.status,
                "created_at": c.created_at,
            })

        return Response(data)

# صفحة الخريطة
def heatmap_page(request):
    return render(request, 'complaints/heatmap.html')


# API الخاصة بالإحداثيات
class HeatmapDataAPIView(APIView):

    def get(self, request):

        complaints = Complaint.objects.all()

        data = []

        for complaint in complaints:
            data.append({
                "latitude": complaint.latitude,
                "longitude": complaint.longitude,
            })

        return Response(data)  
     
from django.db.models import Count

def admin_dashboard(request):

    complaints = Complaint.objects.all()

    total = complaints.count()

    completed = complaints.filter(status='resolved').count()
    in_progress = complaints.filter(status='in_progress').count()
    rejected = complaints.filter(status='rejected').count()

    # نسب
    processed_percent = round((completed / total) * 100) if total else 0
    completion_percent = round(((completed + in_progress * 0.5) / total) * 100) if total else 0
    rejected_percent = round((rejected / total) * 100) if total else 0

    # الأنواع
    trash = complaints.filter(complaint_type='garbage').count()
    road = complaints.filter(complaint_type='road').count()
    light = complaints.filter(complaint_type='lighting').count()

    context = {
        "stats": {
            "total": total,
            "processed_percent": processed_percent,
            "completion_percent": completion_percent,
            "rejected_percent": rejected_percent,
        },
        "categories": {
            "trash": trash,
            "road": road,
            "light": light,
        }
    }

    return render(request, 'complaints/dashboard.html', context)

class DashboardStatsAPIView(APIView):

    def get(self, request):

        complaints = Complaint.objects.all()

        total = complaints.count()
        completed = complaints.filter(status='resolved').count()
        in_progress = complaints.filter(status='in_progress').count()
        rejected = complaints.filter(status='rejected').count()

        return Response({
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "rejected": rejected,
        })