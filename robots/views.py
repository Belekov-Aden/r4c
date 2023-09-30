import datetime
import json

from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_datetime
from django.views.generic import View
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook



from .models import Robot
from orders.models import Order

@method_decorator(csrf_exempt, name='dispatch')
class RobotsView(View):
    def get(self, request):
        robots = {}
        for robot in Robot.objects.all():
            robots['robot'] = model_to_dict(robot)

        data = {'robots': robots}

        return JsonResponse(data)

    def post(self, request):
        data = {'message': 'This is a POST request'}
        return JsonResponse(data)


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            # Валидация данных (здесь можно добавить дополнительные проверки)
            if not model or not version or not created:
                return JsonResponse({'error': 'Invalid data provided'}, status=400)

            # Преобразование даты и времени в нужный формат
            created_datetime = parse_datetime(created)

            # Создание записи о роботе
            robot = Robot(model=model, version=version, created=created_datetime)
            robot.save()

            return JsonResponse({'message': 'Robot created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def generate_excel_report(request):
    # Определяем дату начала и конца последней недели
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    # Создаем новую книгу Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary Report"

    # Заголовок таблицы
    ws.append(["Модель", "Версия", "Количество за неделю"])

    # Получаем уникальные модели и версии роботов за последнюю неделю
    robots = Robot.objects.filter(created__range=(start_date, end_date))
    robot_summary = {}

    for robot in robots:
        model = robot.model
        version = robot.version

        if model not in robot_summary:
            robot_summary[model] = {}
        if version not in robot_summary[model]:
            robot_summary[model][version] = 0

        robot_summary[model][version] += 1

    # Заполняем таблицу данными
    for model, versions in robot_summary.items():
        for version, count in versions.items():
            ws.append([model, version, count])

    # Создаем HTTP-ответ с Excel-файлом
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=robot_summary.xlsx'
    wb.save(response)

    return response




