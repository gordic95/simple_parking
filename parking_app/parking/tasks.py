from celery import shared_task
from django.utils import timezone
import math
from . models import Parkings
from . constants import ONE_HOUR_PRICE
 # Цена часа парковки


@shared_task()
def update_price_on_time():
    # Получаем все активные парковки
    parkings = Parkings.objects.filter(pay=False)

    for parking in parkings:
        # Расчёт цены производится непосредственно методом объекта
        new_price = parking.calculate_price_on_time()

        # Обновляем цену, если изменилась
        if parking.price != new_price:
            parking.price = new_price
            parking.save(update_fields=['price'])