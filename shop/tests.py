from django.test import TestCase
from .models import Category, Product


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Phones",
            slug="phones"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            category=self.category,
            name="iPhone Test",
            slug="iphone-test",
            price=100,
            short_description="Test product"
        )

        self.assertEqual(product.name, "iPhone Test")

        self.assertEqual(product.price, 100)

        self.assertEqual(str(product), "iPhone Test")