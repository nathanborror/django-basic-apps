"""
>>> from django.test import Client
>>> from basic.people.models import Person, Quote, PersonType

>>> c = Client()
>>> p = Person.objects.create(first_name='Nathan', last_name='Borror', slug='nathan-borror')

>>> r = c.get('/people/')
>>> r.status_code
200

>>> r = c.get('/people/nathan-borror/')
>>> r.status_code
200
"""