"""
>>> from django.test import Client
>>> from basic.people.models import Person, Quote, PersonType
>>> from django.core.urlresolvers import reverse

>>> c = Client()
>>> p = Person.objects.create(first_name='Nathan', last_name='Borror', slug='nathan-borror')

>>> r = c.get(reverse('person_list'))
>>> r.status_code
200

>>> r = c.get(reverse('person_detail', kwargs={'slug': 'nathan-borror'}))
>>> r.status_code
200
"""