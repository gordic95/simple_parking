from django.utils import timezone
from math import ceil

from django.db import models
from . constants import ONE_HOUR_PRICE


class Parkings(models.Model):
    time_in = models.DateTimeField(auto_now_add=True, verbose_name="Время въезда")
    pay = models.BooleanField(verbose_name="Статус оплаты", default=False)
    price = models.PositiveIntegerField(verbose_name="Стоимость оплаты", default=0)
    car = models.ForeignKey("Cars", on_delete=models.CASCADE, verbose_name="Автомобиль")


    @property
    def elapsed_time(self):
        """Возвращает прошедшее время с момента въезда"""
        current_time = timezone.now()
        return current_time - self.time_in

    def calculate_price_on_time(self):
        """Рассчитывает стоимость парковки по времени."""
        time_passed = self.elapsed_time
        hours_passed = ceil(time_passed.total_seconds() / 3600)

        if hours_passed <= 1:
            return 0
        else:
            return (hours_passed - 1) * ONE_HOUR_PRICE

    @property
    def actual_price(self):
        """Динамически возвращаемое значение цены с учётом текущего времени."""
        return self.calculate_price_on_time()

    def formatted_actual_price(self):
        """Отформатированное представление реальной стоимости парковки."""
        value = self.actual_price
        return f"{value:,d}" + " ₽"  # Форматируем сумму и добавляем символ рубля

    formatted_actual_price.short_description = "Актуальная стоимость"  # Подпись столбца
    formatted_actual_price.admin_order_field = "price"  # Возможность сортировки по полю price


    def __str__(self):
        return f'{self.car.number} (time_in, pay, price, car.number)'

    class Meta:
        verbose_name = "Парковочное место"
        verbose_name_plural = "Парковочное место"


class Cars(models.Model):
    number = models.CharField(max_length=10, verbose_name="Номер машины", null=True, unique=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"




