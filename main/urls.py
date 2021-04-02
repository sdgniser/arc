from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

pw_reset_view = auth_views.PasswordResetView.as_view(template_name='main/password-reset.htm', email_template_name='main/password-reset-email.htm', subject_template_name='main/pw-reset-subj.txt')

urlpatterns = [
    path('', views.index_view, name='home'),
    #path('login/', views.login, name = 'login'),
    #path('logout/', views.login, name = 'logout'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.htm')),
    path('password_reset/', pw_reset_view),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password-reset-done.htm')),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password-reset-confirm.htm')),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password-reset-complete.htm')),
    path('signup/', views.signup, name='signup'),

    path('', include('authtools.urls')),

    path('u/<uid>/', views.user_view, name='user'),
    path('u/verify/<uid>/<vid>/', views.verify, name='verify'),

    path('s/<abbrev>/', views.school_view, name='school'),
    path('s/<abbrev>/add/', views.add_crs, name='add_crs'),

    path('c/<cd>/', views.course_view, name='course'),
    path('c/<cd>/add/', views.add_itr, name='add_itr'),

    path('c/<cd>/<yr>/<sea>/', views.itr_view, name='itr'),
    path('c/<cd>/<yr>/<sea>/add/', views.add_item, name='add_item'),
    path('c/<cd>/<yr>/<sea>/comment/', views.add_comment, name='comment'),

    path('comm_del/<cid>/', views.delete_comment, name='delete_comment'),

    path('f/<fname>/', views.file_view, name='file'),

    path('report/c/<cid>/', views.report_comment, name='report_comment'),
    path('report/i/<iid>/', views.report_item, name='report_item'),
    path('report/u/<uid>/', views.report_user, name='report_user'),
    
    path('faq/', views.faq, name='faq'),
    path('log/', views.log_view, name='log'),
    path('stat/', views.stat_view, name='stat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
