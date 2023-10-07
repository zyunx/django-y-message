import uuid
from django.http import HttpResponse

import ymessage

from . import ymessage_handlers

def say_hello(request):
    ymessage.compose(type=ymessage_handlers.SAY_HELLO, id=uuid.uuid4(), content={
        'name': 'zyunx', 
    })
    return HttpResponse('OK')
