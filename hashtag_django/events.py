'''
Websockets namespace for updating clients when battles update.

@author:     PJ

'''

from django_socketio.events import Namespace, BaseNamespace, BroadcastMixin

from hashtag_django.models import Battle

# Stores refs to all connections so that we can broadcast battle updates
connections = {}

def updated_battle(battle):
    for conn in connections.itervalues():
        conn.emit("updatedBattle",
                  {"battle_id": battle.id,
                   "left_count": battle.left_hashtag.count,
                   "right_count": battle.right_hashtag.count})

@Namespace('/battles')
class BattleNamespace(BaseNamespace, BroadcastMixin):

    def initialize(self, *args, **kwargs):
        connections[id(self)] = self
        super(BattleNamespace, self).initialize(*args, **kwargs)
        print "new connection"

    def disconnect(self, *args, **kwargs):
        del connections[id(self)]
        super(BattleNamespace, self).disconnect(*args, **kwargs)
        print "lost connection"

    def on_getAllBattles(self, *args, **kwargs):
        print "Get Battles"
        q = Battle.objects.all().select_related(
                                        'left_hashtag', 'right_hashtag')
        battles = [{"battle_id": bat.id,
                    "left_hashtag": bat.left_hashtag.tag,
                    "left_count": bat.left_hashtag.count,
                    "right_hashtag": bat.right_hashtag.tag,
                    "right_count": bat.right_hashtag.count} for bat in q]
        self.emit("allBattles", {"battles": battles})
