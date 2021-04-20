from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    carmake_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car model object
class CarModel(models.Model):
    carmodel_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    
    YEAR_CHOICES = []
    for r in range((now().year), 1979, -1):
        YEAR_CHOICES.append((r,r))
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

    year = models.IntegerField(choices=YEAR_CHOICES, default=now().year)
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    def __str__(self):
        return self.carmake.name + " " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
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

# <HINT> Create a plain Python class `DealerReview` to hold review data
