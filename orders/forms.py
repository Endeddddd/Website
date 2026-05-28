from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=50)

    card_number = forms.CharField(max_length=50)

    def clean_card_number(self):
        card = self.cleaned_data["card_number"]

        # простая валидация (демо)
        if len(card) < 12:
            raise forms.ValidationError("Номер карты слишком короткий")

        return card