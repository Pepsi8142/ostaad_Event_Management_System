from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create-event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('book-event/<int:event_id>/', views.book_event, name='book_event'),
    path('booked-events/', views.booked_events, name='booked_events'),
]
