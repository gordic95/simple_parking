from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . models import Parkings, Cars
from . serializers import CarSerializer, ParkingSerializer, PaySerializer


class CarList(generics.ListAPIView):
    """Класс, который отвечающий за отображение списка автомобилей"""
    queryset = Cars.objects.all()
    serializer_class = CarSerializer


class CarCreate(generics.CreateAPIView):
    """Класс, который отвечает за создание автомобиля"""
    queryset = Cars.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        """Метод, который добавляет информацию о автомобиле в БД"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not Cars.objects.filter(number=serializer.validated_data['number']).exists():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(f"Автомобиль с номером {serializer.data['number']} успешно создан!", status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(f"Автомобиль с номером {serializer.data['number']} уже существует!", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDetail(generics.RetrieveAPIView):
    """Класс, который отвечает за получение информации о выбраном автомобиле"""
    queryset = Cars.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request, *args, **kwargs):
        """Метод, который получает информацию об определенном автомобиле из БД"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#---------------------------------------------------------------------------


class ParkingList(generics.ListAPIView):
    """Класс, который отображает информацию о парковочных местах"""
    queryset = Parkings.objects.all()
    serializer_class = ParkingSerializer

    def get(self, request, *args, **kwargs):
        if not self.queryset.exists():
            return Response("Все парковочные места свободны", status=status.HTTP_200_OK)
        else:
            count_car_places = self.queryset.count()
            if count_car_places == 100:
                return Response("Все парковочные места заняты", status=status.HTTP_200_OK)
            elif count_car_places < 100:
                return Response(f"{100 - count_car_places} парковочных мест свободно", status=status.HTTP_200_OK)
            if count_car_places % 10 == 1:
                return Response(f"{100 - count_car_places} парковочное место свободно", status=status.HTTP_200_OK)
            elif 1 < count_car_places % 10 <= 4:
                return Response(f"{100 - count_car_places} парковочных места свободно", status=status.HTTP_200_OK)
            else:
                return Response(f"{100 - count_car_places} парковочных мест свободно", status=status.HTTP_200_OK)


#___________Три основных представления: вьезда, оплата, выезд______________
class ParkingCreate(generics.CreateAPIView):
    """Класс, для вьезда авто на парковку"""
    queryset = Parkings.objects.all()
    serializer_class = ParkingSerializer

    def perform_create(self, serializer):
        car_number = serializer.validated_data.get('car').number
        if Parkings.objects.filter(car__number=car_number).exists():
            raise ValidationError({"detail": f'Автомобиль {car_number} уже находится на парковке!'})
        else:
            serializer.save()
            return Response({'message': 'Автомобиль успешно поставлен на парковку!'}, status=201)


class ParkingDetail(generics.RetrieveUpdateAPIView):
    """Класс, для оплаты парковочного места"""
    queryset = Parkings.objects.all()
    serializer_class = ParkingSerializer

    def retrieve(self, request, *args, **kwargs):
        """Метод, который получает информацию об определенном парковочном месте из БД"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        """Метод, который оплачивает парковку"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if instance.pay == False:
                serializer.save(pay=True)
                return Response(f"Автомобиль успешно оплатил парковочное место!", status=status.HTTP_200_OK)
            else:
                return Response(f"Автомобиль уже оплатил парковочное место!", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, *args, **kwargs):
    #     """Метод, который оплачивает парковку"""
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         if instance.pay == False:
    #             serializer.save(pay=True)
    #             return Response(f"Автомобиль успешно оплатил парковочное место!", status=status.HTTP_200_OK)
    #         else:
    #             return Response(f"Автомобиль уже оплатил парковочное место!", status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParkingDelete(generics.DestroyAPIView):
    """Класс, для выезда авто с парковки"""
    queryset = Parkings.objects.all()
    serializer_class = ParkingSerializer



    def delete(self, request, *args, **kwargs):
        """Метод, который удаляет информацию об определенном парковочном месте из БД"""
        instance = self.get_object()
        print(instance)
        if instance.pay == False:
            return Response(f"Автомобиль не оплатил парковочное место!", status=status.HTTP_400_BAD_REQUEST)
        elif instance.pay == True:
            instance.delete()
            return Response(f"Выезд разрешен!", status=status.HTTP_200_OK)

#---------------------------------------------------------------------------



















