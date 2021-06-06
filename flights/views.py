from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    duration = flight.duration 
    if duration >= 60:
        h = int(duration/60)
        m = duration % 60
        duration = str(h) + " hr " + str(m) + " min"
    return render(request, "flights/flight.html", {
        "flight": flight,
        "duration": duration,
        "passengers": passengers,
        "non_passengers": non_passengers
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
