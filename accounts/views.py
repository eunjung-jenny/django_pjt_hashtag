from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as user_login, logout as user_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required

def join(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                messages.success(request, '회원님, 환영합니다.')
                new_user = form.save()
                user_login(request, new_user)
                return redirect('community:index')
            else:
                messages.error(request, '회원가입에 실패하였습니다.')
        else:
            form = CustomUserCreationForm()
        context = {
            'form': form
        }
    else:
        messages.error(request, '이미 로그인되어 있습니다.')
        return redirect('community:index')
    return render(request, 'accounts/form.html', context)

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                messages.success(request, '회원님, 반갑습니다.')
                user_login(request, form.get_user())
                return redirect('community:index')
            else:
                messages.error(request, '로그인에 실패하였습니다.')
        else:
           form = AuthenticationForm()
        context = {
            'form': form
        }
    else:
        messages.error(request, '이미 로그인되어 있습니다.')
        return redirect('community:index')
    return render(request, 'accounts/form.html', context)


def logout(request):
    if request.user.is_authenticated:
        user_logout(request)
    return redirect('community:index')

@login_required
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    context = {
        'person': person
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '회원정보가 성공적으로 변경되었습니다.')
            return redirect('accounts:profile')
        else:
            messages.error(request, '회원정보 변경에 실패하였습니다.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
        else:
            messages.error(request, '비밀번호 변경에 실패하였습니다.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def delete(request):
    request.user.delete()
    messages.error(request, '계정이 삭제되었습니다.')
    return redirect('community:index')

@login_required
def follow(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    if request.user in person.followers.all():
        person.followers.remove(request.user)    
    else:
        person.followers.add(request.user)    

    return redirect('accounts:profile', username)
