from django.shortcuts import render, redirect
from .forms import CustomUserForm
import base64
import io
from PIL import Image 
from django.http import JsonResponse
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages
import requests

def register(request):
    if request.method == 'POST':
        form =  CustomUserForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            
            response = requests.post(
                'http://localhost:8001/encode-face/', 
                files={'image': form.cleaned_data['face_image']},
                timeout=150
                )
            
            if response.status_code == 200:
            
                face_data = response.json()
                
                if not face_data.get('encodings'):
                    form.add_error('face_image', 
                                'No face detected in the uploaded image.')
                    return render(request, 'accounts/register.html', 
                                {'form': form})
            
            user.face_image_encode = face_data['encodings']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/register.html', {'form': form})


def find_user_by_face(encoding):
    import numpy as np
    import face_recognition
    current_encoding = np.array(encoding)
    for user in CustomUser.objects.all():
        if user.face_image_encode != None:
            stored_encoding = np.array(user.face_image_encode)
            match = face_recognition.compare_faces([stored_encoding], current_encoding)[0]
            if match:
                return user
    return None

def face_login(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'error': 'تصویر دریافت نشد'}, status=400)

        try:
            header, data = image_data.split(",", 1)
            image_bytes = base64.b64decode(data)
            image_file = io.BytesIO(image_bytes)
        except Exception as e:
            return JsonResponse({'error': 'فرمت تصویر اشتباه است'}, status=400)


        response = requests.post(
            'http://localhost:8001/encode-face/',
            files={'image': ('face.jpg', image_file, 'image/jpeg')},
            timeout=150
        )
         
        if response.status_code == 200:
            face_data = response.json()
            
            if face_data.get('encodings'):
                user = find_user_by_face(face_data['encodings'])  
                if user:
                    login(request, user)
                    return JsonResponse({'status': 'success', 'redirect_url': '/home/'})
                    
                    
            
        return JsonResponse({'status': 'fail', 
                             'error': 'چهره تشخیص داده نشد'})

    return render(request, 'accounts/face_login.html')



def login_view(request):
    return render(request, 'accounts/login.html')


def home_view(request):
    return render(request , 'accounts/home.html')
