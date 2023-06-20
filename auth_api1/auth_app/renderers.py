from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErrorDeatil' in str(data):
            response=json.dumps({'errros':data})
        else:
            response=json.dumps(data)
        return response