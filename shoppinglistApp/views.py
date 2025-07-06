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
from django.contrib.auth.views import PasswordResetView


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

# Create your views here.

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

logger = logging.getLogger(__name__)

class DebugPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        logger.warning("📨 PasswordResetView triggered for: %s", email)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return super().form_valid(form)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = get_current_site(self.request).domain
        reset_link = f"https://{domain}/reset/{uid}/{token}/"
        logger.warning("🔗 Password reset link: %s", reset_link)

        subject = "Reset your password"
        message = render_to_string("registration/password_reset_email.html", {
            "email": email,
            "domain": domain,
            "site_name": "Your App",
            "uid": uid,
            "user": user,
            "token": token,
            "protocol": "https" if self.request.is_secure() else "http",
        })

        mail = EmailMessage(subject, message, to=[email])
        mail.send()
        logger.warning("✅ Single manual reset email sent to: %s", email)

        return super().form_valid(form)



def test_email_send(request):
    logger.warning("📬 Email send TRIGGERED from test-email view")
    send_mail(
        subject="Test Email",
        message="This is a test email sent from PythonAnywhere.",
        from_email="lucirion.no.reply@gmail.com",
        recipient_list=["lucas_95sjolund@hotmail.com"],
        fail_silently=False,
    )
    return HttpResponse("Test email was sent.")
