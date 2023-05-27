from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from home.models import Contact, Attendance, faces
from datetime import date, datetime
import cv2
import numpy as np
from PIL import Image
import face_recognition
from django.contrib import messages
import os
from django.core.files.base import ContentFile
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import io
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(requests):
    return render(requests, "index.html")
def loginuser(requests):
    if requests.method =="POST":
        username = requests.POST.get("username")
        password = requests.POST.get("password")
        user = authenticate(requests, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(requests, user)
            return redirect("upload")
        else:
            # No backend authenticated the credentials
            return render(requests, "authenticate\loginuser.html")
             
    return render(requests, "authenticate\loginuser.html")

@login_required(login_url='authenticate\loginuser.html')
def upload(requests):
    if not requests.user.is_authenticated:
        return render(requests, 'loginuser.html')
    else:
        if requests.method == "POST":
            name = requests.POST.get('name')
            department = requests.POST.get('dep')
            year = requests.POST.get('yr')
            image = requests.FILES.get('formFile')

            # Create a new instance of the model with the form data
            new_instance = faces(name=name, department=department, year=year, image=image)

            # Save the new instance to the database
            new_instance.save()

            # Return a success message to the user
            return HttpResponse('Upload successful!')
        else:
            return render(requests, "upload.html")
def submit(requests):
    return render(requests, "submit.html")



def logoutuser(requests):
    logout(requests)
    return render(requests, "index.html")
def contact(requests):
    if requests.method == "POST":
        name= requests.POST.get('name')
        email= requests.POST.get('email')
        phone= requests.POST.get('phone')
        desc= requests.POST.get('desc')        
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(requests, 'This message has been sent.')
    return render(requests, "contact.html")



@csrf_exempt
def take_attendance(requests):
    if requests.method == 'POST':
        # Get the name of the student from the form data
        # name = requests.POST['name']
        image_data = requests.POST.get('image')
        name = requests.POST.get('name')

        
        img_binary = base64.b64decode(image_data.split(',')[1])
        img_np = np.frombuffer(img_binary, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        face_locations = face_recognition.face_locations(gray)
        if len(face_locations) > 0:
            # If a face is detected, encode the face and compare it with the known faces
            face_encodings = face_recognition.face_encodings(img, face_locations)
            known_face_encodings = []
            known_face_names = []
            dep=[]
            yr=[]
            for student in faces.objects.all():
                image = face_recognition.load_image_file(student.image.path)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) == 0:
                    print(f"No face detected in {student.name}'s image.")
                else:
                    encoding = encodings[0]
                    known_face_encodings.append(encoding)
                    known_face_names.append(student.name)
                    dep.append(student.department)
                    yr.append(student.year)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    department = dep[first_match_index]
                    year = yr[first_match_index]
                    Attendance.objects.create(name=name, status='Present', department=department, year=year, date=datetime.today(), time=datetime.now().time())
                else:
                    Attendance.objects.create(name=name, status='Absent')
        else:
            # If no face is detected, mark the student as absent
            Attendance.objects.create(name=name, status='Absent')
            return render(requests, 'contact.html')

        # Release the webcam and redirect to the same page
        # video_capture.release()
        return redirect('take_attendance')
    else:
        # Render the attendance form
        return render(requests, 'take_attendance.html')