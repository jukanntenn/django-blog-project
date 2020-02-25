from core.abstracts import AbstractEntry
from django.db import models


class Entry(AbstractEntry):
    pass


class RankableEntry(AbstractEntry):
    rank = models.SmallIntegerField(unique=True)

    class Meta:
        ordering = ["rank"]
