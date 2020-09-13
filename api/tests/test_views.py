import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Product, Store
from ..serializers import StoreSerializer, ProductSerializer
import copy

# initialize the APIClient app
client = Client()


class GetAllProductsTest(TestCase):

    def setUp(self):
        store = Store.objects.create(store_name='Pizza Hut')
        Product.objects.create(
            product_name='Large Pizza', is_available=1, store=store)
        Product.objects.create(
            product_name='Muffin', is_available=0, store=store)

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('get_all_products', kwargs={'store_id': 1}))
        # get data from db
        prods = Product.objects.filter(store_id=1)
        serializer = ProductSerializer(prods, many=True)
        self.assertEqual(json.loads(response.content)['products'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_products_invalid_store(self):
        # get API response
        response = client.get(reverse('get_all_products', kwargs={'store_id': 2}))
        # get data from db
        prods = Product.objects.filter(store_id=2)
        serializer = ProductSerializer(prods, many=True)
        self.assertEqual(json.loads(response.content), {'message': 'store does not exist or there is no product at '
                                                                   'store'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddAllProductsTest(TestCase):
    """ Test module for GET all puppies API """
    store = None
    valid_payload = [
        {
            "product_name": "pizza1",
            "is_available": 0
        },
        {
            "product_name": "pasta",
            "is_available": 1
        }
    ]
    invalid_payload = [
        {
            "kt": "pizza1",
            "axy": 0
        },
        {
            "product_name": "pasta",
            "is_available": 1
        }
    ]

    def setUp(self):
        self.store = Store.objects.create(store_name='Pizza Hut')

    def test_get_all_products(self):
        # get API response
        response = client.post(reverse('add_products',
                                       kwargs={'store_id': 1}),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        with_store = copy.deepcopy(self.valid_payload)

        def op(m, i):
            m['store'] = i
            return m

        [op(m, 1) for m in with_store]

        self.assertEqual(json.loads(response.content)['products'], with_store)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_product_to_invalid_store(self):
        # get API response
        response = client.post(reverse('add_products', kwargs={'store_id': 2}),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')

        self.assertEqual(json.loads(response.content), {'error': 'Store matching query does not exist.'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product_invalid_payload(self):
        # get API response
        response = client.post(reverse('add_products', kwargs={'store_id': 1}),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')

        self.assertEqual(json.loads(response.content), {'error': 'Something terrible went wrong'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
