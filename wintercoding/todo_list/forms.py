from django import forms
from . import models

class TODOForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'due_time': forms.TimeInput(attrs={'class': 'timepicki'}),
            }
        fields = ['title', 'content', 'due_date', 'due_time']

class TODOModifyForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'due_time': forms.TimeInput(attrs={'class': 'timepicki'}),
            }
        fields = ['priority', 'title', 'content', 'due_date', 'due_time', 'status']
