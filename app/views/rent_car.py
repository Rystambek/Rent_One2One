from django.views import View
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Rent_car,Car
from .car import to_dict
import json

def to_rent(rent:Rent_car) -> dict:

    return {
        'id':rent.pk,
        'car_id':rent.car.pk,
        'rent_number':rent.rent_number,
        'car_number':rent.car_number,
        'car_yoqilgi':rent.car_yoqilgi,
        'model':rent.model
    }

class RentView(View):
    def get(self,request:HttpRequest,id) -> JsonResponse:
        try:
            rent = Rent_car.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})

        return JsonResponse(to_rent(rent))

    def post(self,request:HttpRequest,id) -> JsonResponse:
        data_json = request.body.decode()
        data = json.loads(data_json)

        car_id = Car.objects.get(id=id)
        car = to_dict(car_id)['id']

        if not data.get('rent_number'):
            return JsonResponse({'status': 'rent_number is required!'})
        elif not data.get('car_number'):
            return JsonResponse({'status': 'car_number is required!'})
        elif not data.get('car_yoqilgi'):
            return JsonResponse({'status': 'car_yoqilgi is required!'})
        elif not data.get('model'):
            return JsonResponse({'status': 'model is required!'})
        
        rent = Rent_car.objects.create(
            car_id = car,
            rent_number = data['rent_number'],
            car_number = data['car_number'],
            car_yoqilgi = data['car_yoqilgi'],
            model = data['model']
        )

        rent.save()
        return JsonResponse(to_rent(rent))
    
    def put(self, request:HttpRequest,id) -> JsonResponse:
        try:
            rent = Rent_car.objects.get(id = id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        data_json = request.body.decode()
        data = json.loads(data_json)

        if data.get('rent_number'):
            rent.rent_number = data['rent_number']
        if data.get('car_number'):
            rent.car_number = data['car_number']
        if data.get('car_yoqilgi'):
            rent.car_yoqilgi = data['car_yoqilgi']
        if data.get('model'):
            rent.model = data['model']

        rent.save()

        return JsonResponse(to_rent(rent))
    
    def delete(self, request:HttpRequest,id) -> JsonResponse:
        try:
            rent = Rent_car.objects.get(id = id)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        rent.delete()

        return JsonResponse({'status':'ok'})