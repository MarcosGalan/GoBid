# forms.py
import django.db.models
from django import forms

from auctions.models import Auction
from products.models import Item


class BetForm(forms.Form):
    bet_amount = forms.IntegerField()


class AuctionUpdateForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['base_price', 'currency', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(AuctionUpdateForm, self).__init__(*args, **kwargs)

        # Personaliza los widgets o agrega clases CSS si es necesario
        self.fields['base_price'].widget.attrs['class'] = 'input'
        self.fields['currency'].widget.attrs['class'] = 'input'
        self.fields['start_date'].widget.attrs['class'] = 'input'
        self.fields['end_date'].widget.attrs['class'] = 'input'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        if self.instance.item.owner != self.user:
            return False

        if self.cleaned_data['end_date'].date() <= self.cleaned_data['start_date'].date():
            self.add_error('end_date', 'End date must be higher then start date')
            return False

        return valid

    def save(self, commit=True):

        auction = super().save(commit=False)

        if commit:
            auction.save()
        return auction


class AuctionCreateForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['item', 'base_price', 'currency', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(AuctionCreateForm, self).__init__(*args, **kwargs)

        # Personaliza los widgets o agrega clases CSS si es necesario
        self.fields['base_price'].widget.attrs['class'] = 'input'
        self.fields['currency'].widget.attrs['class'] = 'input'
        self.fields['start_date'].widget.attrs['class'] = 'input'
        self.fields['end_date'].widget.attrs['class'] = 'input'
        self.fields['item'].widget.attrs['class'] = 'input'
        self.fields['item'].choices = self.get_item_choices()

    def get_item_choices(self):
        items_user = Item.objects.filter(owner=self.user)
        user_auctions_items = [auction.item for auction in Auction.objects.filter(item__owner=self.user)]
        choices = [element for element in items_user if element not in user_auctions_items]

        return choices

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        if self.instance.item.owner != self.user:
            return False

        if self.cleaned_data['end_date'].date() <= self.cleaned_data['start_date'].date():
            self.add_error('end_date', 'End date must be higher then start date')
            return False

        return valid

    def save(self, commit=True):

        auction = super().save(commit=False)
        if commit:
            auction.save()
        return auction
