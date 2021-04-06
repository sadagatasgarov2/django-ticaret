from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, UserProfile
from product.models import Category
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    setting = Setting.objects.get(pk=3)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'profile': profile,
               }
    return render(request, 'user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Sizin accountunuz guncellendi")
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form
                   }
        return render(request, 'user_update.html', context)


def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)# important
            messages.success(request, 'Sizin sifreniz guncellendi')
            return  HttpResponseRedirect('/user')
        else:
            messages.error(request, "Please correct the errorr")
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {'form': form,
                   'category': category}
    return render(request, 'user_password.html', context)
