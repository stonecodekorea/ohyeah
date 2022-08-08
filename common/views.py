from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from common.forms import UserForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            return redirect('ohyeah:index')
    else :
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})
        