from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report, ZipcodeLatLong
from .forms import ReportForm
from datetime import datetime
from .generate_report import get_geocoding_latitude_longitude
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from geocoding.geocode import  get_latitude_longitude_from_google_maps

from cloud_tasks.queue_report import queue_report

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
            queue_report(form.instance)
        return response

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('airquality:index'))


@csrf_exempt
def generate_report_handler(request):
    print('received report for {0}'.format(request.body))
    return HttpResponse('received report for {0}'.format(request.body))


