from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from home.models import Setting, UserProfile
from product.models import Category
from order.models import Order, OrderProduct
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # important
            messages.success(request, 'Sizin sifreniz guncellendi')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, "Please correct the errorr")
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {'form': form,
                   'category': category}
    return render(request, 'user_password.html', context)


@login_required(login_url='/login')
def orders(request):
    current_user = request.user
    category = Category.objects.all()
    orders = Order.objects.filter(user_id=request.user.id)
    context = {'category': category,
               'orders': orders}
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')
def order_detail(request, id):
    current_user = request.user
    category = Category.objects.all()
    order = Order.objects.get(user_id=request.user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {'category': category,
               'order': order,
               'orderitems': orderitems}
    return render(request, 'user_order_detail.html', context)
