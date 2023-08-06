from django.contrib.auth.models import User

from perestroika.methods import Get, Post, Put, Patch, Delete
from perestroika.resource import DjangoResource


class EmptyResource(DjangoResource):
    pass


class FullResource(DjangoResource):
    get = Get(
        queryset=User.objects.all()
    )

    post = Post(
        queryset=User.objects.all()
    )

    put = Put(
        queryset=User.objects.all()
    )

    patch = Patch(
        queryset=User.objects.all()
    )

    delete = Delete(
        queryset=User.objects.all()
    )


__all__ = [
    "EmptyResource",
    "FullResource",
]
