from django import template
from django.conf import settings
from django.utils.safestring import SafeString
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

@register.filter
def format_by_type(value, field):
    if field in ('IM', 'IM0', 'IM1', 'IM2'):
        return SafeString('<a href="http://byvanck.arkyves.org/imgs/%s"><img src="http://h.arkyves.org/t/%s"></a>' % (value, value))
    if field == 'TI':
        return SafeString('<h1>%s</h1>' % value)
    if field == 'SI':
        return SafeString('<h2>%s</h2>' % value)

    return SafeString(value.encode('utf8')+'<br>')