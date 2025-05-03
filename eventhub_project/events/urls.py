from django.urls import path
from . import views
from events.views import APIView
from .views import EventResource

urlpatterns = [

    path('',views.index, name='index'),
    path('home',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('event/', views.event, name='event'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('super_admin_dashboard/',views.super_admin_dashboard,name='super_admin_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('edit_admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('list_admins/',views.list_admins,name='list_admins'),
    path('profile/', views.profile, name='profile'),
    #
    path('add_event_manager/', views.add_event_manager, name='add_event_manager'),
    
    path('delete/<int:product_id>/',
         views.delete_event_manager, name='delete_event_manager'),
    
    path('update/<int:product_id>/',
         views.update_event_manager, name='update_event_manager'),
    #
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    #
    path('dashboard/', views.event_dashboard, name='dashboard'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('view/<int:event_id>/', views.view_event, name='view_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('birthday2/', views.birthday2, name='birthday2'),
    path('birthday3/', views.birthday3, name='birthday3'),
    path('party1/', views.party1, name='party1'),
    path('party2/', views.party2, name='party2'),
    path('wed1/', views.wed1, name='wed1'),
    path('birthday1/', views.birthday1, name='birthday1'),
    #
    path('api/events/', EventResource.as_view(), name='event_list'),
    path('api/events/<int:event_id>/', EventResource.as_view(), name='event_detail'),


]

