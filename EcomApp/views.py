from django.db import models, transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ProductModel, OrderModel
from .serializers import ProductSerializer, OrderSerializer
from .common import handle_error_log, handle_info_log, APP_NAME, ERROR_MESSAGE
from rest_framework.views import APIView
from django.core.exceptions import ValidationError


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class CreateOrderAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            products = request.data.get('products', [])
            total_price = 0
            extra_values = {'request.data': request.data}
            
            with transaction.atomic():
                for item in products:
                    if 'id' not in item:
                        return Response({"id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
                    if 'quantity' not in item:
                        return Response({"quantity": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
                    # validation for valid quantity
                    if item['quantity'] <= 0:
                        return Response({"error": f"Quantity must be a positive integer. {item['quantity']}"}, status=status.HTTP_400_BAD_REQUEST)
                    product = ProductModel.objects.select_for_update().get(id=item['id'])
                    # validate if we have sufficient stock
                    if product.stock < item['quantity']:
                        return Response({"error": f"Insufficient stock for product {product.name} quantity {item['quantity']}"}, status=status.HTTP_400_BAD_REQUEST)
                    total_price += product.price * item['quantity']   

                order = OrderModel.objects.create(products=products, total_price=total_price, status='pending')
                extra_values['order_data'] = order.__dict__

                handle_info_log("Order submitted successfully.", "CreateOrderAPI -> create",APP_NAME,extra_values=extra_values)

                order_dict = OrderSerializer(order)
                return Response(order_dict.data, status=status.HTTP_201_CREATED)
        except ProductModel.DoesNotExist as ne:
            handle_error_log(ne,"CreateOrderAPI -> create", APP_NAME,extra_values=extra_values)
            return Response({"error" :"Invalid Product id."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            handle_error_log(ve,"CreateOrderAPI -> create", APP_NAME,extra_values=extra_values)
            return Response({'error':ve.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            handle_error_log(e,"CreateOrderAPI -> create", APP_NAME,extra_values=extra_values)
            return Response(ERROR_MESSAGE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)