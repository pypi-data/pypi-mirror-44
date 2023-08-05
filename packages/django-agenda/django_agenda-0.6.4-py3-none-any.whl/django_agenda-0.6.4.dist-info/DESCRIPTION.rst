=============
Django Agenda
=============

|pipeline-badge| |coverage-badge| |pypi-badge|

Django agenda is a django app that allow you to create and book
times in a schedule. Our goal is to handle all the nasty details for
you; like timezones, schedule changes, and whether or not a
specific segment is actually available to be booked.

Installation
------------

First, install via pip (on Windows, replace ``pip3`` with ``pip``)

::

    pip3 install django-agenda

Then, edit your ``settings.py``, adding this line to ``INSTALLED_APPS``

::

   'django_agenda',

Features
--------

* Create recurring availabilities. We should support everything that
  RFC 2445 does.
* Subclass AbstractBooking to create bookings. Bookings will reserve
  time slots, and flag them as busy.
* Uses dynamic foreign keys, so you can relate your availabilities &
  bookings to anything (a user, an office space, a classroom)


.. |pipeline-badge| image:: https://gitlab.com/alantrick/django-agenda/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/django-agenda/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/django-agenda/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/django-agenda/
   :alt: Coverage Status

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django_agenda.svg
   :target: https://pypi.org/project/django-agenda/
   :alt: Project on PyPI


CHANGES
=======

0.6.4
-------

* Fix long description rendering problems on pypi

0.6.3
-----

* Add `django_agenda.version`, drop pbr

0.6.2
-----

* add a related name for the bookings relation

0.6.1
-----

* Bug fix for case where foreign key wasn't called schedule

0.6.0
-----

A major rewrite & simplification. This version works *very* differently
from 0.5, don't expect to migrate easily.

* Time slots are now primarily for marking busy state, and
  availability occurrences are for free times.
* You have to create your own models, subclassing the abstract
  models in django_agenda.models. The good thing about this is
  that this allows us to use real foreign keys instead of
  generic ones.
* To that end, you'll have to migrate the data into your models.
  Django Agenda won't delete any of it's own models, but you'll
  have to migrate the data into the new models that you make.
* Booking validation is now done in AbstractBooking.clean
  instead of AbstractBooking.save. Make sure you call full_clean!
* You can use django_agenda.models.get_free_times to find all the
  free time spans in a particular space of time.

0.5.4
-----

* Add the ability to overlap busy slots

0.5.3
-----

* Add ability to overlap bookings

0.5.2
-----

* Add support for django 2

0.5.1
-----

* Fix bug if the start/end time weren't in the same zone as the availability

0.5.0
-----

* Fix handling of daylight savings

0.4.0–0.4.9
-----------

* Small improvements to the regen method
* Fix problem where `_padding_changed` would crash with big changes
* Improve error messaging
* Fix issue where slots were being skipped during regeneration
* Update config so it works more naturally
* Fix issue where `_padding_changed` would alter same slot multiple times
* Add a method to handle non-static padding values
* Fix problem with app config, and gitlab ci
* Fix bug making overlapping slots when a booking spanned existing slots
* Add support for disallowing duplicate bookings
* Fix instruction formatting in readme
* Rewrite scheduling logic
* Add a reasonable number of tests


