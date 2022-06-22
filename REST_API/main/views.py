from lib2to3.pgen2 import token
from tokenize import Token
from django.shortcuts import redirect, render
import requests
from .models import Party
from .serializers import PartySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .models import User


# Create your views here.
# Get or Create a party
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def party_list(request):
    if request.method == 'GET':
        parties = Party.objects.all()
        serializer = PartySerializer(parties, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PartySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Get, Delete or Update a party
@api_view(['GET', 'PUT', 'DELETE'])
def party_detail(request, pk):
    if request.method == 'GET':
        party = Party.objects.get(pk=pk)
        serializer = PartySerializer(party)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        party = Party.objects.get(pk=pk)
        serializer = PartySerializer(party, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        party = Party.objects.get(pk=pk)
        party.delete()
        return Response(status=204)

# Register a candidate
def register_candidate(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            email=request.POST['email'],
            password=request.POST['password'],
            name=request.POST['name'],
            is_candidate=request.POST['True'],
            party=Party.objects.get(pk=request.POST['party'])
        )
        user.save()
        return redirect('/')

# Register a Voter
def register_voter(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            email=request.POST['email'],
            password=request.POST['password'],
        )

        return redirect('/parties')
    return render(request, 'register.html')

# Login a user
def login_user(request):
    if request.method == 'POST':
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/')
    return render(request, 'login.html')

# Logout a user
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/')

# Vote a candidate
@login_required(login_url='/login/')
def vote(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.POST['email'])
        user.votes += 1
        user.save()
        return redirect('/')

# Results page
def results(request):
    return render(request, 'result.html')


# Home page
def index(request):
    return render(request, 'index.html')
