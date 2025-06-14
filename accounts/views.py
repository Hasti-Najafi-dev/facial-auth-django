from django.shortcuts import render, redirect
from .forms import CustomUserForm
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form =  CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/register.html', {'form': form})

def recognize_face(image_bytes):

    return None

def face_login(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'error': 'تصویر دریافت نشد'}, status=400)

        # Decode base64
        try:
            header, data = image_data.split(';base64,')
            image_bytes = base64.b64decode(data)
        except Exception as e:
            return JsonResponse({'error': 'فرمت تصویر اشتباه است'}, status=400)

        user_id = recognize_face(image_bytes)

        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                login(request, user)
                return JsonResponse({'status': 'success'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'کاربر یافت نشد'}, status=404)
        else:
            return JsonResponse({'error': 'چهره شناسایی نشد'}, status=401)

    return render(request, 'accounts/face_login.html')

def login_view(request):
    return render(request, 'accounts/login.html')
