import json
import random
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse

from django.utils.translation import get_language


# Global Variables
from app.models import Challenges

NOMBRE_INSTITUCION = 'Guerreros de Cristo'

EVALUATION_TYPE_BAD = 1
EVALUATION_TYPE_REGULAR = 2
EVALUATION_TYPE_GOOD = 3
EVALUATION_TYPE_VERY_GOOD = 4
EVALUATION_TYPE_EXCELLENT = 5

EVALUATION_TYPES = (
    (EVALUATION_TYPE_BAD, 'Bad'),
    (EVALUATION_TYPE_REGULAR, 'Regular'),
    (EVALUATION_TYPE_GOOD, 'Good'),
    (EVALUATION_TYPE_VERY_GOOD, 'Very Good'),
    (EVALUATION_TYPE_EXCELLENT, 'Excellent')
)


def generate_file_name(nombre, original):
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    fecha = datetime.now().date()
    hora = datetime.now().time()
    return nombre + fecha.year.__str__() + fecha.month.__str__() + fecha.day.__str__() + \
           hora.hour.__str__() + hora.minute.__str__() + hora.second.__str__() + ext


class MiPaginator(Paginator):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, range=5):
        super(MiPaginator, self).__init__(object_list,
                                          per_page,
                                          orphans=orphans,
                                          allow_empty_first_page=allow_empty_first_page)
        self.range = range
        self.pages = []
        self.first_page = False
        self.last_page = False

    def pages_range(self, page):
        left = page - self.range
        right = page + self.range
        if left < 1:
            left = 1
        if right > self.num_pages:
            right = self.num_pages
        self.pages = range(left, right + 1)
        self.first_page = True if left > 1 else False
        self.last_page = True if right < self.num_pages else False
        self.ellipsis_left = left - 1
        self.ellipsis_right = right + 1


def convertir_fecha(s):
    try:
        return datetime(int(s[-4:]), int(s[3:5]), int(s[:2]))
    except:
        return datetime.now()


def convertir_fecha_month_first(s):
    try:
        return datetime(int(s[-4:]), int(s[:2]), int(s[3:5]))
    except:
        return datetime.now()


def convertir_time(time):
    """
        t: array of integers 0-hour 1-minute
    """
    d = datetime.now().date()
    t = time.split(':')
    return datetime(d.year, d.month, d.day, int(t[0]), int(t[1]))


def bad_json(message=None, error=None, extradata=None):
    """
        Returns an invalid response on json data
    """
    data = {'result': 'bad'}
    lang = get_language()

    if message:
        data.update({'message': message})
    if error:
        if error == 0:
            data.update({"message": bad_request(lang)})
        elif error == 1:
            data.update({"message": error_saving_data(lang)})
        elif error == 2:
            data.update({"message": error_updating_data(lang)})
        elif error == 3:
            data.update({"message": error_deleting_data(lang)})
        elif error == 4:
            data.update({"message": no_permission(lang)})
        elif error == 5:
            data.update({"message": error_generating_information(lang)})
        else:
            data.update({"message": system_error(lang)})
    if extradata:
        data.update(extradata)
    return HttpResponse(json.dumps(data), content_type="application/json")


def ok_json(data=None):
    """
        Returns a valid response on json data
    """
    if data:
        if type(data) == dict and 'result' not in data.keys():
            data.update({"result": "ok"})
    else:
        data = {"result": "ok"}
    return HttpResponse(json.dumps(data), content_type="application/json")


def bad_request(lang='en'):
    if lang == 'en':
        message = 'Bad request'
    elif lang == 'es':
        message = 'Solicitud incorrecta'
    else:
        message = ""
    return message


def error_saving_data(lang='en'):
    if lang == 'en':
        message = 'Error saving data'
    elif lang == 'es':
        message = 'Error al guardar datos'
    else:
        message = ""
    return message


def error_updating_data(lang='en'):
    if lang == 'en':
        message = 'Error updating data'
    elif lang == 'es':
        message = 'Error al actualizar datos'
    else:
        message = ""
    return message


def error_deleting_data(lang='en'):
    if lang == 'en':
        message = 'Error deleting data'
    elif lang == 'es':
        message = 'Error al eliminar datos'
    else:
        message = ""
    return message


def no_permission(lang='en'):
    if lang == 'en':
        message = 'You do not have permission to perform this action'
    elif lang == 'es':
        message = 'Usted no tiene permiso para realizar esta acción'
    else:
        message = ""
    return message


def error_generating_information(lang='en'):
    if lang == 'en':
        message = 'Error generating the information'
    elif lang == 'es':
        message = 'Error al generar la información'
    else:
        message = ""
    return message


def system_error(lang='en'):
    if lang == 'en':
        message = 'System error'
    elif lang == 'es':
        message = 'Error del sistema'
    else:
        message = ""
    return message


def generate_code():
    rand = random.randrange(1000, 9999)
    if Challenges.objects.filter(code=rand).exists():
        generate_code()
    return rand
