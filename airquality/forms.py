from django import forms
from .models import Report
from django.db import models


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['zipcode', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.SelectDateWidget(years=list(range(1970, 2018))),
            'end_date': forms.SelectDateWidget(years=list(range(1970, 2018))),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date <= start_date:
            raise forms.ValidationError("Start date must come before end date")