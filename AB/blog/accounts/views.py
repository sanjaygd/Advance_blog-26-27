from django.contrib.auth import authenticate,login,logout,get_user_model
from django.shortcuts import render,redirect

from .form import UserLoginForm,UserRegisterForm


def login_view(request):
    title = 'Login'
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        # print(request.user.is_authenticated)
        if next:
            return redirect(next)
        return redirect('/post/')


    return render(request, 'blog_app/form.html',{'form':form, 'title':title})


def register_view(request):
    title = "Register"
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request,new_user)
        if next:
            return redirect(next)
        
        return redirect('/post/')
    return render(request, 'blog_app/form.html',{'form':form, 'title':title})


def logout_view(request):
    logout(request)
    return redirect('login')





