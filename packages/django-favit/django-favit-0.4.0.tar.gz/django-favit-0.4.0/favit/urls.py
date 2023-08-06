from django.conf.urls import url

from favit.views import add_or_remove, remove

try:
    urlpatterns = patterns('favit.views',
        url(r'^add-or-remove$', 'add_or_remove', name='favit-add-or-remove'),
        url(r'^remove$', 'remove', name='favit-remove'),
    )
except NameError:
    urlpatterns = [
        url(r'^add-or-remove$', add_or_remove),
        url(r'^remove$', remove),
    ]

