import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder
from django import forms
from django.core.exceptions import ValidationError
from . import models

class TODOForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'due_time': forms.TimeInput(attrs={'class': 'timepicki'}),
            }
        fields = ['title', 'content', 'due_date', 'due_time']

    def clean_due_date(self):
        date = self.cleaned_data['due_date']

        # 마감 기한이 미래로 설정되어 있는지 확인
        if date is not None and date < datetime.date.today():
            raise ValidationError('잘못된 날짜 - 현재 시간보다 미래를 설정해야 함')
        return date

    def __init__(self, *args, **kwargs):
        super(TODOForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'title',
            'content',
            'due_date',
            'due_time',
            ButtonHolder(
                Submit('submit', '만들기', css_class='btn btn-secondary')
            )
        )

class TODOModifyForm(forms.ModelForm):
    class Meta:
        model = models.TODO
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'due_time': forms.TimeInput(attrs={'class': 'timepicki'}),
            }
        fields = ['priority', 'title', 'content', 'due_date', 'due_time', 'status']

    def clean_due_date(self):
        date = self.cleaned_data['due_date']

        # 마감 기한이 미래로 설정되어 있는지 확인
        if date is not None and date < datetime.date.today():
            raise ValidationError('잘못된 날짜 - 현재 시간보다 미래를 설정해야 함')

        return date

    def __init__(self, *args, **kwargs):
        super(TODOModifyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'priority',
            'title',
            'content',
            'due_date',
            'due_time',
            'status',
            ButtonHolder(
                Submit('submit', '수정하기', css_class='btn btn-secondary')
            )
        )