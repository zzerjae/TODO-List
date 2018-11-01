from django import forms
from . import models

class TODOForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        fields = ['title', 'content', 'due_by']
        

class TODOModifyForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        fields = ['priority', 'title', 'content', 'due_by', 'status']
        
