from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from content.models import Content, ContentForm, Menu
from home.models import Setting, UserProfile
from product.models import Category, Comment
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

@login_required(login_url='/login')

def comments(request):
    current_user = request.user
    category = Category.objects.all()
    comments = Comment.objects.filter(user_id=request.user.id)
    context = {'category': category,
               'comments': comments}
    return render(request, 'user_comments.html', context)


def contents(request):
    menu = Menu.objects.all()
    current_user = request.user
    category = Category.objects.all()
    contents = Content.objects.filter(user_id=request.user.id)
    context = {'category': category,
               'contents': contents,
               'menu':menu}
    return render(request, 'user_contents.html', context)


def addcontent(request):
    form = ContentForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keyword = form.cleaned_data['keyword']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.description = form.cleaned_data['description']
            data.type = form.cleaned_data['type']
            data.status = 'False'
            data.save()
            messages.success(request, "cONTENT  basari ile kaydedili")
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Bir yanlislik olmali bir daya deneyin')
            return HttpResponseRedirect('/user/addcontent')
    else:
        current_user = request.user
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = ContentForm()
        context = {'category': category,
                   'form': form,
                   'menu': menu}
        return render(request, 'user_addcontent.html', context)


def editcontent(request, id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "content updated")
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content error')
            return HttpResponseRedirect('/')
    else:
        current_user = request.user
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = ContentForm(instance=content)
        context = {'category': category,
                   'form': form,
                   'menu': menu
        }
        return render(request, 'user_addcontent.html', context)



def deletecontent(request, id):
    content = Content.objects.get(id=id)
    content.delete()
    return HttpResponseRedirect('/user/contents')