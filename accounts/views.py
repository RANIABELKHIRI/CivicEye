from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


User = get_user_model()

# 👇 هذا خاص بعرض صفحة HTML
def login_page(request):
    return render(request, 'accounts/login.html')
def register_page(request):
    return render(request, 'accounts/register.html')
def edit_profile_page(request):
    return render(request, 'accounts/edit_profile.html')



@api_view(['POST'])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    date_of_birth = request.data.get('date_of_birth')
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    username = request.data.get('username')

    # 1. التحقق من البيانات الأساسية
    if not first_name or not last_name:
        return Response({"error": "First name and last name required"}, status=400)

    if not password:
        return Response({"error": "Password is required"}, status=400)

    # 2. لازم email أو phone
    if not email and not phone:
        return Response({"error": "You must provide email or phone"}, status=400)

    # 3. منع التكرار
    if email and User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    if phone and User.objects.filter(phone=phone).exists():
        return Response({"error": "Phone already exists"}, status=400)

    # 4. إنشاء username تلقائي إذا ما دخلتوهش
    if not username:
        username = email if email else phone

    # 5. إنشاء المستخدم
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email if email else None,
        phone=phone if phone else None,
        password=password
    )

    # 6. إضافة تاريخ الميلاد
    user.date_of_birth = date_of_birth
    user.save()

    return Response({"message": "User created successfully"}, status=201)
@login_required
def citizen_home(request):
    return render(request, 'accounts/citizen_home.html')
# تخصيص الصفحة:
@api_view(['POST'])
def login(request):

    print("REQUEST DATA:", request.data)

    identifier = request.data.get('identifier')
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"error": "Missing data"}, status=400)

    # 🔍 نحاول نلقاو user بالإيميل أو الهاتف
    user = User.objects.filter(email=identifier).first()

    if user is None:
        user = User.objects.filter(phone=identifier).first()

    if user is None:
        return Response({"error": "User not found"}, status=404)

    # 🔐 التحقق الصحيح
    if not user.check_password(password):
        return Response({"error": "Wrong password"}, status=400)

    # 🔥 JWT
    refresh = RefreshToken.for_user(user)

    role = getattr(user, "role", "citizen")

    ROLE_REDIRECTS = {
        "citizen": "/core/citizen/home/",
        "service1": "/core/service1/home/",
        "service2": "/core/service2/home/",
        "service3": "/core/service3/home/",
        "admin": "/core/authorities/",
    }

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": role,
        "redirect_url": ROLE_REDIRECTS.get(role, "/")
    })
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user

    if request.method == 'GET':
        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "image": getattr(user, "image", None),
            "bio": getattr(user, "bio", None),
        })

    if request.method == 'PUT':
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)

        if hasattr(user, "bio"):
            user.bio = request.data.get('bio', user.bio)

        if hasattr(user, "image"):
            user.image = request.data.get('image', user.image)

        user.save()

        return Response({"message": "Profile updated successfully"})