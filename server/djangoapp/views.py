from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealerships_from_cloudant, \
                      get_dealer_reviews_from_cloudant, \
                      add_dealer_review_to_cloudant
from .models import CarModel
import random
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_dealerships_from_cloudant()
        context = { "dealerships": dealerships }
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id, dealer_name):
    if request.method == "GET":
        dealer_reviews = get_dealer_reviews_from_cloudant(dealer_id)
        context = {
            "dealer_id": dealer_id,
            "dealer_name": dealer_name,
            "reviews": dealer_reviews
        }
        return render(request, 'djangoapp/dealer_reviews.html', context)

# Create a `add_review` view to submit a review
def add_dealer_review(request, dealer_id, dealer_name):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = { "cars": cars, "dealer_id": dealer_id, "dealer_name": dealer_name }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST" and request.user.is_authenticated:
        form = request.POST
        review = {
            "review_id": random.randint(0, 100),
            "reviewer_name": form["fullname"],
            "dealership": dealer_id,
            "review": form["review"]
        }
        if form.get("purchase"):
            review["purchase"] = True
            review["purchase_date"] = form["purchasedate"]
            car = get_object_or_404(CarModel, pk=form["car"])
            review["car_make"] = car.carmake.name
            review["car_model"] = car.name
            review["car_year"]= car.year
        json_result = add_dealer_review_to_cloudant(review)
        return redirect('djangoapp:dealer_reviews', dealer_id=dealer_id, dealer_name=dealer_name)
