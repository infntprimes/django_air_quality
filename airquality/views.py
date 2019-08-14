from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('airquality:index'))
