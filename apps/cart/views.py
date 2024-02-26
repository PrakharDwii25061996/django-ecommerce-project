from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    CartAddProductSerializer, CartRemoveProductSerializer
)


class CartAddProductAPIView(generics.UpdateAPIView):
    serializer_class = CartAddProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        try:
            cart = self.get_object()
            serializer = self.get_serializer(
                cart, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': "Added Product Sucessfully",
                    'data': serializer.data,
                    'status': status.HTTP_200_OK
                }
            return Response(
                    {
                        'errors': serializer.errors,
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                    }
               )
        except Exception as e:
            return Response(
                {
                    'errors': e,
                    'message': "Profile not updated",
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartRemoveProductAPIView(generics.UpdateAPIView):
    serializer_class = CartRemoveProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
