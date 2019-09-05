from .models import Report, AirQualityReport
from .forms import ReportForm
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode, quote_plus
from datetime import datetime, date
from django.contrib.auth import get_user_model, get_user
from django_air_quality.privatesettings import GOOGLE_API_KEY, TASKS_KEY
from django.core.cache import cache
from geocoding.geocode import get_latitude_longitude_from_google_maps
from airquality import generate_report
import googlemaps
import random
import time
import json

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

class TestGeocoding(TestCase):

    def test_connect_to_google_api(self):
        api_key = GOOGLE_API_KEY
        try:
            gm = googlemaps.Client(key=api_key)
            self.assertIsNotNone(gm)
        except:
            self.assertTrue(False)


    def test_retrieve_latitude_longitude_from_google_api(self):
        """
        In production, we might want to use some sort of mock api,
        since each call is costing $$$ (but negligible for scope of project)
        """
        gm = googlemaps.Client(key=GOOGLE_API_KEY)
        zipcode = '85259'

        latitude,longitude = get_latitude_longitude_from_google_maps(zipcode)

        self.assertIsNotNone(latitude)
        self.assertIsNotNone(longitude)
        self.assertTrue(latitude > 32 and latitude < 35)
        self.assertTrue(longitude < -110 and longitude > -113)

class TestRedisCache(TestCase):
    def test_adding_key(self):
        random.seed(datetime.now())
        randomString = "test" + str(random.randrange(999999))
        cache.set(str(randomString),"1", timeout=30)
        self.assertIsNotNone(cache.get(str(randomString)))
        self.assertEquals(cache.get(str(randomString)), "1")

    def test_key_can_expire(self):
        random.seed(datetime.now())
        randomString = "test" + str(random.randrange(999999))

        cache.set(str(randomString), "1", timeout=1)
        time.sleep(2) #sleep to let cache expire, this case can potentially be run asynchronously if performance constraints of tests demand it
        self.assertIsNone(cache.get(str(randomString)))

class TestAirQualityReportCreation(TestCase):
    def test_creating_report(self):

        #create Test report form. to be used for foreign key assignment in our AirQualityReport object below
        rep = Report.objects.create(
            zipcode='85259',
            start_date='2014-01-01',
            end_date='2015-01-01',
            datetime_created=datetime.now(),
            created_by=None
        )
        rep.save()


        #simulate a cloud_tasks payload
        payload = json.dumps({
            'zipcode': str('85259'),
            'start_date': str('2014-01-01'),
            'end_date': str('2015-01-01'),
        })

        #call generate report with a payload in the same style our cloud_tasks function will
        generate_report.create_report(payload)

        self.assertIsNotNone(AirQualityReport.objects.get_queryset())

        aq_report = AirQualityReport.objects.get_queryset()[0]

        self.assertTrue(aq_report.AQI_green_days > 50)
        self.assertTrue(aq_report.AQI_yellow_days > 1)

        self.assertIsNotNone(aq_report.binary_raw_file)
        self.assertIsNotNone(aq_report.userRequest)

