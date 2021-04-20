from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealerships_from_cloudant, \
                      get_dealer_reviews_from_cloudant, \
                      add_dealer_review_to_cloudant
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
    context = {}
    if request.method == "GET":
        dealerships = get_dealerships_from_cloudant()
        dealer_names = '<div></div>'.join([dealer.full_name for dealer in dealerships])
        return HttpResponse(dealer_names)
        # context['dealerships'] = dealerships
        # return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealer_reviews = get_dealer_reviews_from_cloudant(dealer_id)
        reviews = ' '.join([review.review for review in dealer_reviews])
        return HttpResponse(reviews)

# Create a `add_review` view to submit a review
def add_dealer_review(request):
    context = {}
    if request.method == "POST" and request.user.is_authenticated():
        add_dealer_review_to_cloudant(request.POST)
    return redirect('djangoapp:about')
