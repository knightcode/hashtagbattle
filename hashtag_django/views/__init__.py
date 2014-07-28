'''
Main logic for the front end of the hashtag battles app. The app consists of
two endpoints: (1) a full page that displays both the form to create new
battles and the view of existing, on-going ones, and (2) an AJAX endpoint for
submitting the two hashtags of a new battle, which just returns a JSON object
string.

@author:     PJ

'''
import json
import os
import subprocess
import sys

from django.http.response import HttpResponse
from django.views.generic import TemplateView, View

from hashtag_django.models import BattleTag, Battle
from hashtag_django.stream_handler import ensure_running_updater, new_battle

# Reference to the stream_handler background script
# This is a quick-n-dirty approach to background processing
#background_script = None


class BattlesView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, *args, **kwargs):
        global background_script
        context = super(BattlesView, self).get_context_data(*args, **kwargs)
        ensure_running_updater()
        return context


class CreateBattleView(View):
    """
      AJAX call for creating a battle and returning a JSON object to the
      client. This is written in a way to facilitate the creation of a super
      class that would collect the generic things needed to return a JSON
      string
    """
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        try:
            context = self.proccess_request(request, *args, **kwargs)
            response = HttpResponse(json.dumps(context),
                                    content_type='application/json')
            return response
        except Exception:
            pass

    def proccess_request(self, request, *args, **kwargs):
        left = request.GET.get('left', None)
        right = request.GET.get('right', None)

        # Sanitize inputs
        if not left and not right:
            print "Missing params: {0} {1}".format(left, right)
        print "Got {0} {1}".format(left, right)
        left = left.lower()
        right = right.lower()
        if left[0] != '#':
            left = "#{0}".format(left)
        if right[0] != '#':
            right = "#{0}".format(right)

        # Create objects in the database
        left_tag = BattleTag.objects.create(tag=left)
        right_tag = BattleTag.objects.create(tag=right)
        battle = Battle.objects.create(left_hashtag=left_tag,
                                       right_hashtag=right_tag)
        new_battle(battle)
        return {'success': True,
                'error_msg': '',
                'battle_id': battle.id,
                'left_hashtag': left,
                'left_count': 0,
                'right_hashtag': right,
                'right_count': 0
                }
