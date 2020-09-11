from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Product, Store
from .serializers import ProductSerializer, ProductsSerializer
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

@api_view(["GET"])
def welcome(request):
    content = {"message": "Welcome to the BookStore!"}
    return JsonResponse(content)

@api_view(["GET"])
def get_products(request, store_id):
    try:
        products = Product.objects.filter(store_id=store_id)
        if len(products) == 0:
            raise ObjectDoesNotExist('store does not exist or there is no product at store')
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'message': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def add_products(request, store_id):
    # user = request.user.id
    data = json.loads(request.body)

    try:
        store = Store.objects.get(id=store_id)

        productObjects = [Product(product_name=m['product_name'],
                      is_available=m['is_available'],
                      store=store) for m in data]

        products = Product.objects.bulk_create(productObjects)
        serializer = ProductsSerializer(products, many=True)
        return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)