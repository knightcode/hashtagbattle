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

    def get_battle(self):
        if hasattr(self, 'left_battle'):
            return self.left_battle
        else:
            return self.right_battle


class Battle(models.Model):
    """
      Represents a battle between two hashtags.
    """
    left_hashtag = models.OneToOneField(BattleTag, related_name="left_battle")
    right_hashtag = models.OneToOneField(BattleTag, related_name="right_battle")
