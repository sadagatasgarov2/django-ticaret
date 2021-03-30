from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from order.models import ShopCartForm, ShopCart
from product.models import Category


def index(request):
    return HttpResponse('Order App')


@login_required(login_url='/login')
def addtocart(request, id):
    current_user = request.user
    url = request.META.get('HTTP_REFERER')
    checkproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Urun basari ile sebete eklenmistir")
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Urun basari ile sebete eklenmistir")
        return HttpResponseRedirect(url)
    messages.warning(request, "Urun ekleme sirasinda hata olustu")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    context = {'shopcart': shopcart,
               'category': category,
               'total': total}
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    shopcart = ShopCart.objects.filter(id=id)
    shopcart.delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Silinidi urun carttan")
    return HttpResponseRedirect('/order/shopcart')
