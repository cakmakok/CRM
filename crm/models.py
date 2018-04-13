from django.core import validators
from django.db import models
import re


class Address(models.Model):
    zip_code = models.IntegerField('ZIP Code')
    house_number = models.CharField('House Number', max_length=40, blank=True)
    street_name = models.CharField('Street Name', max_length=40, blank=True)
    city = models.CharField('City', max_length=40, blank=True)


class Product(models.Model):

    DATA = 1
    VOICE = 2
    BUNDLE = 3

    PRODUCT_TYPE = (
        ('DATA', 'Data'),
        ('VOICE','Voice'),
        ('BUNDLE','Bundle'),
    )
    product_name = models.CharField('Product Name', max_length=40, blank=True)
    product_type = models.IntegerField('Product Type', choices=PRODUCT_TYPE)

class Customers(models.Model):

    FEMALE = 1
    MALE = 2
    GENDERS = (
        (FEMALE, 'Female'),
        (MALE, 'Male')
    )

    first_name = models.CharField('First Name', max_length=40, blank=True)
    last_name = models.CharField('Last Name', max_length=40, blank=True)
    email = models.EmailField('E-mail Address', blank=True)
    phone = models.CharField('Telephone', max_length=30, blank=True,
                             validators=[
                                 validators.RegexValidator(re.compile('^\+?1?\d{9,15}$'),
                                                           'Enter a valid phone number.', 'invalid'), ])
    date_of_birth = models.DateField('Date of Birth')
    gender = models.IntegerField(choices=GENDERS)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Subscription(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField('Subscription Expiry')
    balance = models.IntegerField('Balance')
