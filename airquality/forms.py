from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    """
    Creates a form for the user to enter their location and target dates to generate a report
    """
    class Meta:
        model = Report
        fields = ['zipcode', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.SelectDateWidget(years=list(range(1970, 2017+1))),
            'end_date': forms.SelectDateWidget(years=list(range(1970, 2017+1))),
        }

    def clean(self):
        """
        verifies that start_date comes before end_date when a user submits a form
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date <= start_date:
            raise forms.ValidationError("Start date must come before end date")
