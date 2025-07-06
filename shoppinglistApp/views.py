# © 2025 Lucas Jasper
# Licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import EmailOnlySignUpForm
from .models import ShoppingItem

from django.http import HttpResponse
from django.core.mail import send_mail
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return '/list/'

def signup(request):
    if request.method == 'POST':
        form = EmailOnlySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shopping_list')
    else:
        form = EmailOnlySignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'shoppinglistApp/home.html')

@login_required
def shopping_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            ShoppingItem.objects.create(title=title, user=request.user)
        return redirect('shopping_list')
    items = ShoppingItem.objects.filter(user=request.user)
    return render(request, 'shoppinglistApp/shopping_list.html', {'items': items})

def toggle_completed(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    item.completed = not item.completed
    item.save()
    return redirect('shopping_list')

@require_http_methods(["GET", "POST"])
def edit_item(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            item.title = new_title
            item.save()
            return redirect('shopping_list')
    return render(request, 'shoppinglistApp/edit_item.html', {'item': item})

def delete_item(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    item.delete()
    return redirect('shopping_list')

# Japanese language version below

class CustomLoginJPView(LoginView):
    template_name = 'login_jp.html'
    def get_success_url(self):
        return '/list/jp/'
    
def custom_logout(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER', '')
    if '/jp/' in referer or referer.endswith('/jp'):
        return redirect('home_jp')
    return redirect('home')

def signup_jp(request):
    if request.method == 'POST':
        form = EmailOnlySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shopping_list_jp')
    else:
        form = EmailOnlySignUpForm()
    return render(request, 'registration/signup_jp.html', {'form': form})

def home_jp(request):
    return render(request, 'shoppinglistApp/home_jp.html')

@login_required
def shopping_list_jp(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            ShoppingItem.objects.create(title=title, user=request.user)
        return redirect('shopping_list_jp')
    items = ShoppingItem.objects.filter(user=request.user)
    return render(request, 'shoppinglistApp/shopping_list_jp.html', {'items': items})

def toggle_completed_jp(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    item.completed = not item.completed
    item.save()
    return redirect('shopping_list_jp')

@require_http_methods(["GET", "POST"])
def edit_item_jp(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            item.title = new_title
            item.save()
            return redirect('shopping_list_jp')
    return render(request, 'shoppinglistApp/edit_item_jp.html', {'item': item})

def delete_item_jp(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id)
    item.delete()
    return redirect('shopping_list_jp')

from django.http import HttpResponse
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def test_email_send(request):
    logger.warning("📬 Email send TRIGGERED from test-email view")
    send_mail(
        subject="Test Email",
        message="This is a test email sent from PythonAnywhere.",
        from_email="lucirion.no.reply@gmail.com",
        recipient_list=["your@email.com"],
        fail_silently=False,
    )
    return HttpResponse("Test email was sent.")
