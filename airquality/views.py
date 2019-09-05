from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from geocoding.geocode import  get_latitude_longitude_from_google_maps
from cloud_tasks import queue_report
from django_air_quality.privatesettings import TASKS_KEY
from geocoding.geocode import get_latitude_longitude_from_google_maps
from airquality import generate_report
import json


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'airquality/index.html'
    login_url = '/login/'

    def get_queryset(self):
        """

        :return:
        """
        return None


class LoginView(generic.TemplateView):
    template_name = 'airquality/login.html'

class ReportCreateView(LoginRequiredMixin, generic.CreateView):
    """
    creates a view to generate a new report via a form
    """
    model = Report
    login_url = '/login/'
    form_class = ReportForm
    template_name = 'airquality/new_report_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.datetime_created = datetime.now()
        response = super().form_valid(form)
        if (response.status_code == 302):
            # form was submitted successfully, begin processing a report via a cloud task
            queue_report.queue_report(form.instance)
        return response

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('airquality:index'))


@csrf_exempt
def generate_report_handler(request):
    """
    To be called from cloud tasks, will actually create a report
    """
    if (str(TASKS_KEY) not in str(request.body.decode())):
        print("request to report handler was made with an incorrent/missing key")
        return HttpResponseForbidden()
    else:
        print('received report for {0}'.format(str(request.body)))

        generate_report.create_report(request.body.decode()) ####starts the process of report creation

        return HttpResponse('report for {0} COMPLETED'.format(request.body))