import json

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
import product
from content.models import Menu, Content, CImages
from home.forms import SearchForm, SignupForm
from home.models import Setting, ContactForm, ContactFormMassage, UserProfile
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=3)
    sliderdata = Product.objects.all()[:5]
    category = Category.objects.all()
    menu = Menu.objects.all()
    news = Content.objects.filter(type = 'haber').order_by('-id')[:4]
    announcement = Content.objects.filter(type='duyuru').order_by('-id')[:4]
    dayproduct = Product.objects.all()[:4]
    lastproduct = Product.objects.all().order_by('-id')[:4]
    randomproduct = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    university = "Karabuk University"
    dept = "Computer Engineering"
    context = {'setting': setting,
               'sliderdata': sliderdata,
               'category': category,
               'menu': menu,
               'news':news,
               'announcement': announcement,
               'page': 'home',
               'dayproduct': dayproduct,
               'lastproduct': lastproduct,
               'randomproduct': randomproduct,
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=3)
    context = {'setting': setting, 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=3)
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'referanslar.html', context)


def iletisim(request):
    category = Category.objects.all()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMassage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajiniz basari ile gonderilmistir")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=3)
    form = ContactForm()
    context = {'setting': setting,
               'category': category,
               'form': form}
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context = {'category': category,
               'products': products,
               'categorydata': categorydata}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product_detail = Product.objects.get(pk=id)
    image = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'category': category,
               'product_detail': product_detail,
               'image': image,
               'comments': comments
               }
    return render(request, 'product_detail.html', context)


def content_detailbdksbkfjd(request, id, slug):
    category = Category.objects.all()
    product_detail = Product.objects.filter(category_id=id)
    link = '/product/' + str(product_detail[0].id) + '/' + product_detail[0].slug
    context = {'category': category,
               }
    # return render(request, 'products.html', context)
    return HttpResponse(link)
    # return HttpResponseRedirect(link)


def content_detail(request, id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    content = Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id = id)
    context = {'category': category,
               'menu':menu,
               'content': content,
               'images': images
               }
    return render(request, 'content_detail.html', context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {'products': products,
                       'category': category}
            return render(request, 'product_search.html', context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "Login hatasi sifre ve ya kullanici adi hatali")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        user = User()
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            userprofile = UserProfile()
            userprofile.user_id = request.user.id
            userprofile.image = "images/users/user.jpg"
            userprofile.save()
            messages.success(request, "Basari ile kayit oldunuz")
            return HttpResponseRedirect('/')

    form = SignupForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form
               }
    return render(request, 'signup.html', context)


def menu(request, id):
    content = Content.objects.get(menu_id=id)
    if content:
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    else:
        messages.success(request, "HAta !!! Ilgili icerik bulunamai")
        link = '/'
        return HttpResponseRedirect(link)
