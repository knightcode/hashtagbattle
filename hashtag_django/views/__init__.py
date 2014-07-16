
import json
import os
import subprocess
import sys

from django.http.response import HttpResponse
from django.views.generic import TemplateView, View

from hashtag_django.models import BattleTag, Battle

# Reference to the stream_handler background script
# This is a quick-n-dirty approach to background processing
background_script = None


class BattlesView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, *args, **kwargs):
        global background_script
        context = super(BattlesView, self).get_context_data(*args, **kwargs)
        context['battles'] = Battle.objects.all().select_related(
                                        'left_hashtag', 'right_hashtag')
        if len(context['battles']) > 0 and background_script is None:
            background_script = subprocess.Popen([sys.executable,
                            'scripts/stream_handler.py'])
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
        
        if not left and not right:
            print "Missing params: {0} {1}".format(left, right)
        print "Got {0} {1}".format(left, right)
        left = left.lower()
        right = right.lower()
        print "Creating {0} {1}".format(left, right)
        left_tag = BattleTag.objects.create(tag=left)
        right_tag = BattleTag.objects.create(tag=right)
        print "Done"
        Battle.objects.create(left_hashtag=left_tag,
                                       right_hashtag=right_tag)
        pass