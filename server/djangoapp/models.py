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
        return "Car Make: " + self.name

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
    year = models.DateField(blank=False)

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
    TYPES = [
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
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPES,
        default=SEDAN
    )
    def __str__(self):
        return "Car Make: " + self.carmake.name + ", " + \
               "Car Model: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
