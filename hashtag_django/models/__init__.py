#
# Django DB Models for Hashtag Battle App
#

from django.db import models


class BattleTag(models.Model):
    """
      Represents a hashtag in a battle. Hashtags can belong to multiple
      battles, each with its own count
    """
    tag = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

class Battle(models.Model):
    left_hashtag = models.ForeignKey(BattleTag, related_name="left_battles")
    right_hashtag = models.ForeignKey(BattleTag, related_name="right_battles")
