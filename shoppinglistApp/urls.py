from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import DebugPasswordResetView

urlpatterns = [
    # Core app pages
    path('', views.home, name='home'),
    path('jp/', views.home_jp, name='home_jp'),
    path('signup/jp/', views.signup_jp, name='signup_jp'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/jp/', views.CustomLoginJPView.as_view(), name='login_jp'),
    path('logout/', views.custom_logout, name='logout'),

    # Shopping list
    path('list/', views.shopping_list, name='shopping_list'),
    path('list/jp/', views.shopping_list_jp, name='shopping_list_jp'),
    path('toggle/<int:item_id>/', views.toggle_completed, name='toggle_completed'),
    path('jp/toggle/<int:item_id>/', views.toggle_completed_jp, name='toggle_completed_jp'),
    path('edit/<int:item_id>', views.edit_item, name='edit_item'),
    path('jp/edit/<int:item_id>', views.edit_item_jp, name='edit_item_jp'),
    path('remove/<int:item_id>', views.delete_item, name='delete_item'),
    path('jp/remove/<int:item_id>', views.delete_item_jp, name='delete_item_jp'),

    # Password reset
    path(
        'password-reset/',
        DebugPasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
