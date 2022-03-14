from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, 'default_app/home.html')

def signupuser(request):
	name_taken_error_msg = 'That username is already taken.  Please choose a new username.'
	password_mismatch_error_msg = 'Passwords did not match.'
	if request.method == 'GET':
		return render(request, 'default_app/signup.html', {'form':UserCreationForm()})
	else:
		# Create new user:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('home')
			except IntegrityError:
				return render(request, 'default_app/signup.html', {'form':UserCreationForm(), 'error':name_taken_error_msg})
		else:
			return render(request, 'default_app/signup.html', {'form':UserCreationForm(), 'error':password_mismatch_error_msg})


@login_required
def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')


def loginuser(request):
	bad_credentials_error_msg = 'Unrecognised login details.'
	if request.method == 'GET':
		return render(request, 'default_app/login.html', {'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'default_app/login.html', {'form':AuthenticationForm(), 'error':bad_credentials_error_msg})
		else:
			login(request, user)
			return redirect('home')
