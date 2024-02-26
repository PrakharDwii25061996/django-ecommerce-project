
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView

import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .serializers import (
    ProductSerializer, PaymentSerializer,
    TokenSerializer, CategorySerializer,
    SubCategorySerializer
)
from .models import Product, Category, SubCategory
from .pagination import ProductListPagination

stripe.api_key = settings.STRIPE_SECRET_KEY


class CategoryAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'data': serializer.data,
                'message': "Successfully created Category",
                'status': status.HTTP_200_OK
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'errors': serializer.errors,
            'message': "Category not created!"
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        response = {
            'data': serializer.data,
            'message': "All Categories retreived",
            'status': status.HTTP_200_OK
        }
        return Response(response, status=status.HTTP_200_OK)


class SubCategoryAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SubCategory.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'data': serializer.data,
                'message': "Successfully created Category",
                'status': status.HTTP_200_OK
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'errors': serializer.errors,
            'message': "Category not created!"
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        serializer = SubCategorySerializer(sub_categories, many=True)
        response = {
            'data': serializer.data,
            'message': "All Categories retreived",
            'status': status.HTTP_200_OK
        }
        return Response(response, status=status.HTTP_200_OK)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = (IsAuthenticated,)
    # pagination_class = ProductListPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request, *args, **kwargs):
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductUpdateRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.ObjectDoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('id'))
        if not product:
            response = {
                "message" : "Product Does not exist."
            }
            return Response(response)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('id'))
        if not product:
            response = {
                "message" : "Product Does not exist."
            }
            return Response(response)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('id'))
        if not product:
            response = {
                "message" : "Product Does not exist."
            }
            return Response(response)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('id'))
        if not product:
            response = {
                "message" : "Product Does not exist."
            }
            return Response(response)
        product.delete()
        response = {
            "message": "Your Product is successfully deleted."
        }
        return Response(response)


class PaymentCreateAPIView(generics.ListCreateAPIView):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data.get('token')
            # product_id = serializer.data.get('product_id')
            # product_price = serializer.data.get('price')
            # product_name = serializer.data.get('name')
            # checkout_session = stripe.checkout.Session.create(
            #     payment_method_types =  ['card', 'acss_debit'],
            #     metadata =  {"product_id": product_id},
            #     mode = 'payment',
            #     line_items = [
            #         {
            #             "price_data": {
            #                 "currency": "usd",
            #                 "unit_amount": int(float(product_price)) * 100,
            #                 "product_data": {
            #                     "name": product_name
            #                 },
            #             },
            #             "quantity": 1,
            #         }
            #     ],
            #     success_url = settings.PAYMENT_SUCCESS_URL,
            #     cancel_url = settings.PAYMENT_CANCEL_URL,
            # )

            # test_payment_intent = stripe.PaymentIntent.create(
            #     amount=serializer.data.get('price'),
            #     currency='usd', 
            #     payment_method_types=['card'],
            #     receipt_email='prakhardwivedi360@gmail.com'
            # )

            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                source=token,
                description='Example charge',
            )

            response_data = {
                'message': "Payment Successfull",
                'token': token
            }

            return Response(data=response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessAPIView(APIView):

    def get(self, request, *args, **kwargs):
        response = {
            "message": "Your Payment is Successfully!"
        }
        return Response(data=response)


class PaymentCancelAPIView(APIView):

    def get(self, request, *args, **kwargs):
        response = {
            "message": "Your Payment is Failed!"
        }
        return Response(data=response)
