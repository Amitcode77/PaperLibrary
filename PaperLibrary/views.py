from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                               label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control form-group"}),
                               label="Password", required=True)


@csrf_exempt
def login_process(request, action=None):
    context = dict()
    if request.method == "POST" and action == "log-in":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("main.html")
    elif request.method == "POST" and action == "log-out":
        logout(request)
    # GET
    context['main'] = LoginForm()
    return render(request, "login.html", context)
