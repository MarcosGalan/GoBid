from django import forms

from core.models import CustomUser
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['product', 'name', 'description', 'image', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(ItemForm, self).__init__(*args, **kwargs)

        # Personaliza los widgets o agrega clases CSS si es necesario
        self.fields['product'].widget.attrs['class'] = 'input'
        self.fields['name'].widget.attrs['class'] = 'input'
        self.fields['description'].widget.attrs['class'] = 'input'
        self.fields['image'].widget.attrs['class'] = 'input'
        self.fields['price'].widget.attrs['class'] = 'input'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid  # If the basic validation fails, no need to proceed with custom validation

        return valid

    def save(self, commit=True):

        item = super().save(commit=False)
        item.owner = self.user

        if commit:
            item.save()
        return item
