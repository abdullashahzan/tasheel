from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
from .CVision import *
from django.http import JsonResponse
import random, time
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "main/signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            UserProfile.objects.create(user=user, status="User").save()
            messages.success(request, 'Account created successfully')
            return redirect('main:signin')
    return render(request, "main/signup.html")

def signout(request):
    logout(request)
    return redirect('main:signin') 

def index(request):
    road = Road.objects.first()
    webuser = UserProfile.objects.get(user=request.user)
    return render(request, "main/home.html", {
        'road': road,
        'webuser': webuser,
    })

def services(request):
    return render(request, "main/services.html")

def modify_road(request, option):
    print(option)
    road = Road.objects.first()
    if option == "switch":
        if road.direction == 0 or road.direction == 2 or road.direction == 3:
            road.direction = 1
        else:
            road.direction = 0
    elif option == 'double':
        road.direction = 2
    elif option == 'stop':
        road.direction = 3
    else:
        road.direction = 0
    road.save()
    return redirect('main:home')

def tell_crowd(request):
    crowd_info = random.randint(0,3)
    return JsonResponse({'crowd_info': crowd_info})

def change_camera(request):
    road = Road.objects.first()
    if road.camera >= 0 and road.camera < 1:
        road.camera += 1
    else:
        road.camera = 0
    road.save()
    return redirect('main:home')

def video_stream():
    road = Road.objects.first()

    path1 = "/home/shahzan/Documents/Codes/Django/tasheel/main/test_videos/Hajj 2023 Short video .mp4"
    path2 = "/home/shahzan/Documents/Codes/Django/tasheel/main/test_videos/Safa Marwa Sayee Makkah #shorts.mp4"
    
    if road.camera == 0:
        video_path = path1
    elif road.camera == 1:
        video_path = path2


    while True:
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                # Break the inner loop and restart the video if it has ended
                break
            
            # Encode the frame as a JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            # Control the frame rate
            time.sleep(0.03)  # Adjust for approximately 30 fps

        # Release the capture and reopen it to loop
        cap.release()

# View to return the video stream
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')
