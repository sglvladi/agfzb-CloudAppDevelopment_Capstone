import logging

from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate

from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, save_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
class AboutUsView(generic.TemplateView):
    template_name = 'djangoapp/about.html'


# Create a `contact` view to return a static contact page
class ContactUsView(generic.TemplateView):
    template_name = 'djangoapp/contact.html'


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# NOTE: I am using the DealershipsListView Instead!!!
# def get_dealerships(request):
#     if request.method == "GET":
#         url = "https://bef3097c.eu-gb.apigw.appdomain.cloud/api/dealership"
#         # Get dealers from the URL
#         dealerships = get_dealers_from_cf(url)
#         # Concat all dealer's short name
#         dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
#         # Return a list of dealer short name
#         return HttpResponse(dealer_names)


class DealershipsListView(generic.ListView):
    template_name = 'djangoapp/dealership_list.html'
    context_object_name = 'dealerships'

    def get_queryset(self):
        dealerships = get_dealers_from_cf()
        return dealerships


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealerships_details(request, dealer_id):
    if request.method == "GET":
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(dealer_id=dealer_id)
        dealer = get_dealer_by_id_from_cf(dealer_id=dealer_id)
        context = {
            'reviews': reviews,
            'dealer_id': dealer_id,
            'dealer': dealer
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            dealer = get_dealer_by_id_from_cf(dealer_id=dealer_id)
            cars = CarModel.objects.all()
            context = {
                'dealer': dealer,
                'cars': cars
            }
            return render(request, 'djangoapp/add_review.html', context)
        else:
            return redirect('djangoapp:login')
    elif request.method == "POST":
        model = get_object_or_404(CarModel, id = request.POST['car'])
        review = {
            'name': request.user.first_name + ' ' + request.user.last_name,
            'id': 2,
            'dealership': dealer_id,
            'review': request.POST['content'],
            'purchase': request.POST['purchasecheck']=='on',
            'purchase_date': model.year.year,
            'car_make': model.make.name,
            'car_model': model.name,
            'car_year': model.year.year
        }
        if request.user.is_authenticated:
            save_review(review)
        return HttpResponseRedirect(reverse('djangoapp:dealer_details', args=(dealer_id,)))



