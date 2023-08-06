from django.urls import reverse
from django.utils.six.moves.urllib import parse
from djactasauth.backends import ActAsBackend


def act_as_login_url(auth, act_as, **query):
    username = ActAsBackend.sepchar.join([auth, act_as])
    return get_login_url(username=username, **query)


def get_login_url(**query):
    return reverse('login') + '?' + parse.urlencode(query)
