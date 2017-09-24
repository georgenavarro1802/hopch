from django.shortcuts import render

from hopch.settings import MEDIA_URL, MEDIA_ROOT, DEBUG


def index(request):
    return render(request, "index.html",
                  {
                      'title': 'Guerreros de Cristo',
                      'domain_url': "{}{}".format('http://', request.get_host()),
                      'media_url': MEDIA_URL
                  })
