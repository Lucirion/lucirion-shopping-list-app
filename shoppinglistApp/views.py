# © 2025 Lucas Jasper
# Licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)

import logging

from django.contrib.auth import (
    login, logout, get_user_model
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView, PasswordResetView
)
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site

from .forms import EmailOnlySignUpForm, NoOpPasswordResetForm
from .models import ShoppingItem

logger = logging.getLogger(__name__)

# ─── Core App Views ──────────────────────────────────────────────────────────

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return '/list/'

def signup(request):
    form = EmailOnlySignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('shopping_list')
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


# ─── Japanese Views ───────────────────────────────────────────────────────────

class CustomLoginJPView(LoginView):
    template_name = 'login_jp.html'
    def get_success_url(self):
        return '/list/jp/'

def custom_logout(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER', '')
    return redirect('home_jp' if '/jp/' in referer or referer.endswith('/jp') else 'home')

def signup_jp(request):
    form = EmailOnlySignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('shopping_list_jp')
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


# ─── Custom Password Reset ────────────────────────────────────────────────────

class DebugPasswordResetView(PasswordResetView):
    form_class = NoOpPasswordResetForm
    template_name = 'registration/password_reset_form.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        logger.warning("📨 Reset requested for: %s", email)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return self.render_to_response(self.get_context_data(form=form))

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = get_current_site(self.request).domain
        reset_link = f"{self.request.scheme}://{domain}/reset/{uid}/{token}/"
        logger.warning("🔗 Reset link: %s", reset_link)

        subject = "Reset your password"
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': token,
            'protocol': self.request.scheme,
        })
        logger.debug("📩 Email body:\n%s", message)

        mail = EmailMessage(
            subject,
            message,
            from_email="lucirion.no.reply@gmail.com",
            to=[email],
        )
        try:
            mail.send(fail_silently=False)
            logger.warning("✅ Email sent to %s", email)
        except Exception as e:
            logger.error("🚨 Email send failed: %s", e)

        return redirect('password_reset_done')


# ─── Manual Email Test Endpoint ───────────────────────────────────────────────

# def test_email_send(request):
#    logger.warning("📬 Email send TRIGGERED from test-email view")
#    send_mail(
#        subject="Test Email",
#        message="This is a test email sent from PythonAnywhere.",
#        from_email="lucirion.no.reply@gmail.com",
#        recipient_list=["lucas_95sjolund@hotmail.com"],
#        fail_silently=False,
#    )
#    return HttpResponse("Test email was sent.")
