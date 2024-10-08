from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from django.db.models import Q
from .models import Record


# Create your views here.

def home(request):
	records = Record.objects.all()

	# check if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		#Authenticate
		user = authenticate(request, username=username, password=password)

		if user is not None: 
			login(request, user)
			messages.success(request, "You succesfully logged in!")
			return redirect('home')
		else:
			messages.success(request, "There was an error logging in, please try again.")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})


def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged out.")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You have successfully registered!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})


	return render(request, 'register.html', {'form':form})


def song_record(request, pk):
	if request.user.is_authenticated: 
		song_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'song_record':song_record})
	else: 
		messages.success(request, "You must be logged in to view page.")
		return redirect('home')


def delete_record(request, pk):
	if request.user.is_authenticated: 
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record deleted succesfully.")
		return redirect('home')
	else: 
		messages.success(request, "Log in first to delete record.")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated: 
		if request.method == "POST": 
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record added.")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else: 
		messages.success(request, "Login first to add record.")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated: 
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record updated.")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else: 
		messages.success(request, "Login first to update record.")
		return redirect('home')


def search_records(request):
    if request.user.is_authenticated:  # User must be logged in to check user records
        query = request.GET.get('q')  # Get the search query from the request
        song_records = []

        if query:
            first_word = query.split()[0] if query.split() else '' #gets first word

            # Filter records where the first word of the song title matches
            song_records = Record.objects.filter(artist_name__istartswith=first_word).order_by('song_title')
            # Get all matching records and sort alphabetically  by artist name

        return render(request, 'search_records.html', {'song_records': song_records})

    else:
        messages.success(request, "You must be logged in to search records.")
        return redirect('home')
