from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm, Comment


def index(request):
    return HttpResponse("My Product Page")


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.success(request, "formuniz basari ile gonderildi")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz gonderilmedi")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def deletecomment(request, id):
    comment = Comment.objects.filter(id=id, user_id=request.user.id)
    comment.delete()
    messages.success(request, "Silinidi Commentcarttan")
    return HttpResponseRedirect('/user/comments')
