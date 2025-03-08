from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ProductModel, OrderModel
from django.core.exceptions import ValidationError
from django.urls import reverse
import json


# Unit Tests for Models
class ProductModelTest(TestCase):
    def test_create_product(self):
        """Test that product created successfully with correct data"""
        product = ProductModel.objects.create(name="Test Product", description="Sample", price=10.0, stock=5)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.stock, 5)

    def test_product_negative_price(self):
        """Test that product raises exception with incorrect data"""
        product = ProductModel(name="Invalid Product", description="Negative price", price=-5.0, stock=5)
        with self.assertRaises(ValidationError):  # Expecting validation error
            product.full_clean()  # This enforces validators
            product.save()


class OrderModelTest(TestCase):
    def setUp(self):
        self.product = ProductModel.objects.create(name="Laptop", description="Gaming Laptop", price=1000.0, stock=10)
    
    def test_create_order_with_sufficient_stock(self):
        """Test that stock is deducted correctly when an order is placed"""

        # Order 3 units (stock should reduce from 10 -> 7)
        order_data = [{"id": self.product.id, "quantity": 3}]
        order = OrderModel.objects.create(products=order_data, total_price=3000.0)

        # Refresh product from DB to get updated stock
        self.product.refresh_from_db()

        # Ensure stock is deducted properly
        self.assertEqual(self.product.stock, 7, "Stock should be reduced correctly")

    def test_create_order_with_insufficient_stock(self):        
        """Test that stock never goes below zero"""

        # Trying to order more than available stock (stock=10, ordering=12)
        order_data = [{"id": self.product.id, "quantity": 12}]

        with self.assertRaises(Exception):  # Assuming validation raises an exception
            OrderModel.objects.create(products=order_data, total_price=8000.0)

        # Refresh product from DB
        self.product.refresh_from_db()

        # Ensure stock remains unchanged
        self.assertEqual(self.product.stock, 10, "Stock should not be reduced if order fails")  


# Integration Tests for API's
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.product_data = {"name": "Phone", "description": "Smartphone", "price": 500.0, "stock": 10}
        self.product = ProductModel.objects.create(**self.product_data)
        
    def test_list_products(self):
        """Test that Get products api response"""
        response = self.client.get(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_product(self):
        """Test that Create products api response"""
        response = self.client.post(reverse('products-list'), {"name": "Tablet", "description": "Android Tablet", "price": 300.0, "stock": 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Tablet")


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.product = ProductModel.objects.create(name="Headphones", description="Wireless", price=50.0, stock=5)
        self.content_type = "application/json"
    
    def test_place_valid_order(self):
        """Test that Place order api response"""
        order_data = {"products": [{"id": self.product.id, "quantity": 2}], "total_price": 100.0}
        response = self.client.post(reverse('orders'), data=json.dumps(order_data), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
    
    def test_order_with_insufficient_stock(self):
        """Test that place order api with insufficient stock"""
        order_data = {"products": [{"id": self.product.id, "quantity": 10}], "total_price": 500.0}
        response = self.client.post(reverse("orders"), data=json.dumps(order_data), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_order_with_negative_quantity(self):
        """Test that place order api with negative quantity"""
        order_data = {"products": [{"id": self.product.id, "quantity": -2}], "total_price": -100.0}
        response = self.client.post(reverse("orders"), data=json.dumps(order_data), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Quantity must be a positive integer", str(response.data))
    
    def test_concurrent_order_placing(self):
        """Test that place order api with concurrent request"""
        order_data = {"products": [{"id": self.product.id, "quantity": 3}], "total_price": 150.0}
        response1 = self.client.post(reverse("orders"), data=json.dumps(order_data), content_type=self.content_type)
        response2 = self.client.post(reverse("orders"), data=json.dumps(order_data), content_type=self.content_type)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertIn(response2.status_code, [status.HTTP_400_BAD_REQUEST])
