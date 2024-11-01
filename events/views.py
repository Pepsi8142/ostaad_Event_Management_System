from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Event, Booking
from .forms import EventForm, UserProfileForm
from django.contrib import messages


# Create your views here.
def homepage(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    events = Event.objects.all()
    if query:
        events = events.filter(name__icontains=query) | events.filter(location__icontains=query) | events.filter(date__icontains=query)

    if category:
        events = events.filter(category=category)

    user_bookings = []
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'events/homepage.html', {'events': events, 'user_bookings': user_bookings, 'query': query, 'selected_category': category})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('booked_events')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'events/profile.html', {'form': form})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('homepage')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    is_booked = Booking.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_booked': is_booked
    })


@login_required
def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.organizer != request.user and not request.user.is_staff:
        return redirect('homepage')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form})


@login_required
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.organizer == request.user or request.user.is_staff:
        event.delete()
    return redirect('homepage')


@login_required
def book_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if Booking.objects.filter(event=event).count() < event.capacity:
        if not Booking.objects.filter(user=request.user, event=event).exists():
            Booking.objects.create(user=request.user, event=event)
            messages.success(request, "You have successfully booked the Event!")
        else:
            messages.warning(request, "You have already booked the Event!")
    else:
        messages.error(request, "Sorry, this Event is fully booked!")
    return redirect('homepage')


@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/booked_events.html', {'bookings': bookings})
