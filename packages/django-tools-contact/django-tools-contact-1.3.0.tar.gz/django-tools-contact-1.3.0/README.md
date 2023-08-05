# Django Tools Contact

Django Tools Contact is a simple Django app to manage a company contact information and contacts
requests from a form

## Installation

1. Install with pip install `django-tools-contact`.

2. Add `djtools.contact` to your INSTALLED_APPS setting like this:
```
INSTALLED_APPS = [
    ...
    'djtools.contact',
]
```

3. Add your Google Maps API key nd your contact information in your project settings:
```
DJTOOLS_CONTACT_GMAPS_APIKEY = "ABCDE123"
DJTOOLS_CONTACT_SITE_DOMAIN = "www.example.com"
DJTOOLS_CONTACT_MAIL_FROM = "no-reply@example.com"
DJTOOLS_CONTACT_MAIL_TO = ["admin@example.com"]

```

4. It has a dependency over `django-recaptcha`. Follow their instructions as well:
[Django ReCaptcha](https://github.com/praekelt/django-recaptcha).


5. You can use the `ContactRequestView` like this:
```
from djtools.contact.views import ContactRequestView


urlpatterns = [
    path('contact/', ContactRequestView.as_view(), name='contact'),
]
```

6. Run `python manage.py migrate` to create the contact models.

7. If you want to show the comapny contact information in the same page as the contact form
you need to enable this setting `DJTOOLS_CONTACT_INFO=True`, then start the development server and
visit http://127.0.0.1:8000/admin/ to create add the contact information (you'll need the Admin app
enabled).

8. Visit http://127.0.0.1:8000/contact/ to see the contact information and send contact requests.

## References
https://github.com/pydanny/cookiecutter-djangopackage/
