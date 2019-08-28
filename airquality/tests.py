from .models import Report
from .forms import ReportForm
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode, quote_plus
from datetime import datetime, date
from django.contrib.auth import get_user_model, get_user


class NewReportFormTests(TestCase):
    def test_that_form_tests_run(self):
        self.assertTrue(True)  # meta af, also completely unnecessary

    def setUpUser(self):
        self.user = get_user_model().objects.create_user(username='tester', password='Testing!')
        login = self.client.login(username='tester', password='Testing!')

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
            'start_date': '2017-12-31',
            'end_date': '2017-01-01',
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
        form_data = {
            'zipcode': 'O1950',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '8522x',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'zipcode': '!8525',
            'start_date': '1970-01-01',
            'end_date': '2017-01-01',
        }

        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_new_report_error_message_start_date_not_before_end_date(self):
        c = Client()
        user = get_user_model().objects.create_user(username='tester', password='Testing!')
        login = c.login(username='tester', password='Testing!')

        response = c.post('/new/',
                          {
                              'zipcode': '12345',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1980',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '1980'})
        # 'end_date': '2017-01-01'
        # 'start_date': '1970-01-01'
        self.assertNotEqual(response.status_code, '302')
        self.assertContains(response, "start date must come before end date")

        response = c.post('/new/',
                          {
                              'zipcode': '01950',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1979',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '1970'})

        self.assertNotEqual(response.status_code, '302')
        self.assertContains(response, "start date must come before end date")

    def test_new_report_error_message_zipcode_not_numeric_not_5_digits(self):
        c = Client()
        user = get_user_model().objects.create_user(username='tester', password='Testing!')
        login = c.login(username='tester', password='Testing!')
        response = c.post('/new/',
                          {
                              'zipcode': 'X1950',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1970',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '2017'})

        self.assertContains(response, 'zipcode must be 5 numeric digits')
        response = c.post('/new/',
                          {
                              'zipcode': '111950',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1970',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '2017'})

        self.assertContains(response, 'Ensure this value has at most 5 characters')


    def test_new_report_error_message_dates_out_of_range(self):
        #this shouldn't even be possible if the form is filled out via UI, but is possible if a user were to send a manual POST request
        c = Client()
        user = get_user_model().objects.create_user(username='tester', password='Testing!')
        login = c.login(username='tester', password='Testing!')
        response = c.post('/new/',
                          {
                              'zipcode': '12345',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1969',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '2017'})

        self.assertContains(response, 'must be in the range [1970,2017]')

        response = c.post('/new/',
                          {
                              'zipcode': '12345',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '2018',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '2017'})

        self.assertContains(response, 'must be in the range [1970,2017]')

        response = c.post('/new/',
                          {
                              'zipcode': '12345',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1970',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '1969'})

        self.assertContains(response, 'must be in the range [1970,2017]')

        response = c.post('/new/',
                          {
                              'zipcode': '12345',
                              'start_date_month': '1',
                              'start_date_day': '1',
                              'start_date_year': '1970',
                              'end_date_month': '1',
                              'end_date_day': '1',
                              'end_date_year': '2018'})

        self.assertContains(response, 'must be in the range [1970,2017]')
