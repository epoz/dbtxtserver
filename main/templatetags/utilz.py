from django import template
from django.conf import settings
from PIL import Image
import json, os

register = template.Library()

@register.simple_tag
def seadragonlevels(image):
    buf = []
    try:
        img = Image.open(os.path.join(settings.IMAGE_CACHE_PATH, image))
    except IOError:
        # The filename 'IIHIM_-661110976.jpg' is the 'Image Not Available pic'
        img = Image.open(os.path.join(settings.IMAGE_CACHE_PATH, 'IIHIM_-661110976.jpg'))
    width, height = img.size
    buf.append({'url': '/imgs/%s' % image,
        'height': height, 'width': width 
    })

    return '''levels:%s''' % json.dumps(buf)