from users import views as user_views
from django.contrib.auth import views as auth_views
from django.urls import path,include

urlpatterns = [
    
    path('register/', user_views.register, name = 'register'),
    path('login/', user_views.login, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'deal/Views/index.html', next_page='index'), name = 'logout'),
    path('profile', user_views.profile, name = 'profile'),
    path('profile', user_views.profile, name = 'profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset' ),
   
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done' ),
    path('password-reset/Confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm' ),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete' ),
    path('profile/', user_views.profile,name='profile' ), 
    path('accounts/', include('allauth.urls')),
]