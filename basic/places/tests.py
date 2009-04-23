"""
>>> from django.test import Client
>>> from basic.places.models import PlaceType, City, Point, Place

>>> c = Client()
>>> type = PlaceType.objects.create(title='Coffeehouse', slug='coffeehouse')
>>> city = City.objects.create(city='Lawrence', state='KS', slug='lawrence-ks')
>>> point = Point.objects.create(city=city)
>>> place = Place.objects.create(point=point, title='Wheatfields', slug='wheatfields', status=1)
>>> place.place_types.add(type)
>>> place.save()

>>> r = c.get('/places/')
>>> r.status_code
200

>>> r = c.get('/places/wheatfields/')
>>> r.status_code
200

>>> r = c.get('/places/cities/')
>>> r.status_code
200

>>> r = c.get('/places/cities/lawrence-ks/')
>>> r.status_code
200

>>> r = c.get('/places/types/')
>>> r.status_code
200

>>> r = c.get('/places/types/coffeehouse/')
>>> r.status_code
200
"""