from django.shortcuts import redirect, render
from parkingapp.models import *
from django.contrib import messages
import cv2
import pickle
import numpy as np
import cvzone as cvzone


# Create your views here.


def HomePage(request):
    return render(request, 'Home.html')

def AboutPage(request):
    return render(request, 'about.html')

def ContactPage(request):
    return render(request, 'contact.html')

def LoginPage(request):
    user_email = 'admin@gmail.com'
    user_pwd = 'admin'
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        if email == user_email and pwd == user_pwd:
            messages.success(request, 'Login Successfull..!')
            return redirect('dashboard')
        elif email == user_email and pwd != user_pwd:
            messages.error(request, 'Password Incorrect..')
            return redirect('login')
        else:
            messages.error(request, 'Login Failed Check your Email and Password..!')
            return redirect('login')
    return render(request, 'loginpage.html')

def DashboardPage(request):
    return render(request, 'dashboard.html')

def MyProfilePage(request):
    return render(request, 'myprofile.html')

def SmartParkingPage(request) :
    if request.method == 'POST' and request.FILES['upload_file']:
        video = request.FILES['upload_file']
        Upload_File.objects.create(Video = video)
        messages.success(request, 'Smart Prking Executed Successfully...')
        return redirect('video')

    return render(request, 'smartcarparking.html')

def VideoPage(request):
    a = Upload_File.objects.last()
    print(a.Video, 'video path')
    b=str(a.Video)
    cap = cv2.VideoCapture('media/'+b)
    with open('parkingapp\CarParkPos', 'rb') as f:
        posList = pickle.load(f)
    width, height = 107, 48
    
    def check_parking_space(img_pro):
        space_counter = 0
    
        for pos in posList:
            x, y = pos
    
            img_crop = img_pro[y:y + height, x:x + width]
            count = cv2.countNonZero(img_crop)
    
            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                space_counter += 1
            else:
                color = (0, 0, 255)
                thickness = 2
    
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
    
        cvzone.putTextRect(img, f'Free: {space_counter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))
    
    
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
        success, img = cap.read()
    
        if not success:
            break
    
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    
        check_parking_space(img_dilate)
    
        cv2.imshow("Image", img)
    
        if cv2.waitKey(1) == 27:  # Press Esc key to exit
            break
    cv2.destroyAllWindows()
    Upload_File.objects.order_by('pk').first().delete()
    return render(request, 'smartcarparking.html')




