from .models import Report
from .forms import ReportForm
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode, quote_plus
from datetime import datetime, date
from django.contrib.auth import get_user_model, get_user


class NewReportFormTests(TestCase):
    def test_that_form_tests_run(self):
        self.assertTrue(True)  # meta af, also completely unnecessary

    def setUp(self):
        user = get_user_model().objects.create_user('admin')

    def test_new_report_form_valid(self):
        formData = {
            'zipcode': '12345',
            'start_date': '1970-01-01',
            'end_date': '2017-12-31'
        }
        form = ReportForm(data=formData)
        self.assertTrue(form.is_valid())

    def test_new_report_form_invalid_range(self):

        form_data = {
            'zipcode': '12345',
            'start_date': '1969-12-31',
            'end_date': '1969-12-31'
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '12345',
            'start_date': '2018-01-01',
            'end_date': '2018-01-02'
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_invalid_start_date(self):
        # start date should be in range [1970,2017], try both edges
        form_data = {
            'zipcode': '12345',
            'start_date': '1969-12-31',
            'end_date': '2017-01-01'
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        ##again, with start_date
        form_data = {
            'zipcode': '12345',
            'start_date': '2018-01-01',
            'end_date': '2017-01-01'
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_invalid_end_date(self):
        # end date should be in range [1970,2017], try both edges
        form_data = {
            'zipcode': '12345',
            'start_date': '1970-01-01',
            'end_date': '2018-01-01',
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '12345',
            'start_date': '1970-01-01',
            'end_date': '1969-01-01',
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_start_date_after_end_date(self):
        # start date must come before end date
        form_data = {
            'zipcode': '12345',
            'start_date': '1970-01-02',
            'end_date': '1970-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '12345',
            'start_date': '2017-01-01',
            'end_date': '2017-12-31',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_start_date_is_equal_to_end_date(self):
        form_data = {
            'zipcode': '12345',
            'start_date': '2017-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_zipcode_not_5_characters(self):
        form_data = {
            'zipcode': '001950',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '1950',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_form_zipcode_not_numeric(self):

        formData = {
            'zipcode': 'O1950',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=formData)
        self.assertFalse(form.is_valid())

        formData = {
            'zipcode': '8522x',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=formData)
        self.assertFalse(form.is_valid())


        formData = {
            'zipcode': '!8525',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=formData)
        self.assertFalse(form.is_valid())
