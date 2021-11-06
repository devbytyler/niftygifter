from django.conf import settings

def process(request):
    return {
        'settings': settings,
    }
