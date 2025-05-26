from django.shortcuts import render, redirect
from userauth.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from core.views import home

user = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        print('User Registered')
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account was created successfully, {username}")
            login(request, new_user)  # Use the saved user directly
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'signup.html', context)





# def register_view(request):
#     if request.method == "POST":
#         print('User Registered')
#         form = UserRegisterForm(request.POST)
        
#         if form.is_valid():
#             new_user = form.save() 
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"Your account was created successfully, {username}")
#             new_user = authenticate(username=username, password=form.cleaned_data.get('password1'))
#             if new_user is not None:
#                 login(request, new_user)
#                 return redirect('home')
#     else:
#         form = UserRegisterForm()
    
#     context = {'form': form}
#     return render(request, 'signup.html', context)





def login_view(request):
    
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in")
        return redirect('accountPage')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("accountPage")
        else:
            messages.warning(request, "User Does Not Exist")
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def account_page(request):
    return render(request, 'page-account.html')