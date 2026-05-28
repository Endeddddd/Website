from django.test import TestCase
from .forms import CheckoutForm


class CheckoutFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            "address": "Test street",
            "city": "Berlin",
            "postal_code": "12345",
            "phone": "123456789",
            "card_number": "123456789012"
        }

        form = CheckoutForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_card(self):
        form_data = {
            "address": "Test street",
            "city": "Berlin",
            "postal_code": "12345",
            "phone": "123456789",
            "card_number": "123"
        }

        form = CheckoutForm(data=form_data)

        self.assertFalse(form.is_valid())