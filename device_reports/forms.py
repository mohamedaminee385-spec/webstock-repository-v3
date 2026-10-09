from django import forms
from .models import DeviceReport

class DeviceReportForm(forms.ModelForm):
    class Meta:
        model = DeviceReport
        fields = ['device', 'issue_type', 'description', 'attachment']
        widgets = {
            'device': forms.Select(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border'
            }),
            'issue_type': forms.Select(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Provide detailed information about the issue...',
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border'
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }