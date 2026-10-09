from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'title', 'category', 'quantity', 'status',
            'screen_size', 'processor', 'ram_gb', 'print_speed_ppm',
            'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'screen_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'processor': forms.TextInput(attrs={'class': 'form-control'}),
            'ram_gb': forms.NumberInput(attrs={'class': 'form-control'}),
            'print_speed_ppm': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }