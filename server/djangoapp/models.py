from django.db import models
from django.utils.timezone import now

# Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    carmake_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

# Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    YEAR_CHOICES = []
    for r in range((now().year), 1979, -1):
        YEAR_CHOICES.append((r,r))
    # TYPES
    SEDAN = 'sedan'
    COUPE = 'coupe'
    SUV = 'suv'
    TRUCK = 'truck'
    VAN = 'van'
    WAGON = 'wagon'
    SPORTS = 'sports_car'
    LUX = 'luxury_car'
    HYBRID = 'hybrid_electric'
    DIESEL = 'diesel'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (COUPE, 'Coupe'),
        (SUV, 'SUV'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
        (WAGON, 'Wagon'),
        (SPORTS, 'Sports Car'),
        (LUX, 'Luxury Car'),
        (HYBRID, 'Hybrid/Electric'),
        (DIESEL, 'Diesel'),
    ]
    carmodel_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    year = models.IntegerField(choices=YEAR_CHOICES, default=now().year)
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    def __str__(self):
        return self.carmake.name + " " + self.name

# Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
    def __str__(self):
        return "Dealer: " + self.full_name

# Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase,
                 purchase_date, review, sentiment):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        return "Review: " + self.review
