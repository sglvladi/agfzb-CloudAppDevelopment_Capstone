from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=50, default='Car make name')
    description = models.CharField(max_length=200, default='Car make description')
    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50, default='Car model name')
    dealer_id = models.IntegerField(null=True)

    SEDAN = 'sedan'
    WAGON = 'wagon'
    SUV = 'suv'
    HATCHBACK = 'hatch'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (HATCHBACK, 'Hatchback'),
        (WAGON, 'Wagon'),
        (SUV, 'SUV'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SEDAN)

    year = models.DateField(null=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.make.name, self.name)




# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, car_make, car_model, car_year, name, purchase, purchase_date, review,
                 sentiment='neutral'):
        self.id = id
        self.dealership = dealership
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review