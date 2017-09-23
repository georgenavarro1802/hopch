from django.shortcuts import render

from hopch.settings import MEDIA_URL, MEDIA_ROOT, DEBUG


def index(request):
    data = {'title': 'Guerreros de Cristo'}
    if DEBUG:
        data['domain_url'] = "{}{}".format('http://', request.get_host())
    else:
        if 'www' not in request.get_host():
            data['domain_url'] = "{}{}".format('https://www.', request.get_host())

    data['media_url'] = MEDIA_URL
    return render(request, "index.html", data)
