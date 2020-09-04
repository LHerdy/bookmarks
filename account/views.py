from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistratioForm
from .models import Profile
from .forms import LoginForm, UserRegistratioForm, UserEditForm, ProfileEditForm
from django.contrib import messages

def user_login(request):
    if request.method == 'Post':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                 username=cd['username'],
                                 password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Autenticação realizda com sucesso!')
                else:
                    return HttpResponse('Conta desabilitada')
            else:
                return HttpResponse('Login inválido')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistratioForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password( user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
         user_form = UserRegistratioForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instace=request.user.profile, data=request.POST,
                                       file=request.FILES)
        if user_form.is_valid()() and profile_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Atualização realizada com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar seu perfil!')
    else:
        user_form - UserEditForm(instance=request.user)
