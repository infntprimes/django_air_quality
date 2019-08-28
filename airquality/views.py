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
    # @method_decorator(csrf_exempt)
    # def dispatch(self,request,*args,**kwargs):
    #     return super(ReportCreateView, self).dispatch(request, *args, **kwargs)
    """
    creates a view to generate a new report via a form
    """
    model = Report
    #  fields = ['zipcode', 'start_date', 'end_date']
    login_url = '/login/'
    form_class = ReportForm
    template_name = 'airquality/new_report_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.datetime_created = datetime.now()
        response = super().form_valid(form)

        return response

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('airquality:index'))

