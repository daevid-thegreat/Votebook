from django.shortcuts import redirect, render
from .models import Subject
from .serializers import subjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


###### APIs ########

# Get all parties or Create a party
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def subject_list(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = subjectSerializer(subjects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        serializer = subjectSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Get, Delete or Update a party
@api_view(['GET', 'PUT', 'DELETE'])
def subject_detail(request, id_subject):
    if request.method == 'GET':
        subject = Subject.objects.get(id_subject=id_subject)
        serializer = subjectSerializer(subject)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        party = Subject.objects.get(id_subject=id_subject)
        serializer = subjectSerializer(party, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        party = Subject.objects.get(id_subject=id_subject)
        party.delete()
        return Response(status=204)


###### PAGES ########

# Register a User
def register_voter(request):
    if request.method == 'POST':
        User.objects.create_user(email=request.POST['email'], password=request.POST['password'])
        return redirect('/signin')
    return render(request, 'register.html')

# Login a user
def login_user(request):
    if request.method == 'POST':
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            return redirect('/login')
    return render(request, 'login.html')

# Logout a user
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/')

#Create subject
@login_required(login_url='/login/')
def create_subject(request):
    if request.method == 'POST':
        Subject.objects.create()
        return redirect('/campaigns')
    return render(request, 'create-subject.html')

# Results page
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects':subjects})

# single subject page
def subject_detail(request, id_subject):
    subject = Subject.objects.filter(id_subject = id_subject)
    return render(request, 'detail.html', {'subject':subject})

# Home page
def index(request):
    return render(request, 'index.html')

#Profile
def profile(request):
    token = request.user.auth_token.key
    return render(request, 'profile.html' , {'token': token})