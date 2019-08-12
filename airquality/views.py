from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse
# from .models import Question, Choice
from django.contrib.auth import logout


class IndexView(generic.ListView):
    template_name = 'airquality/index.html'

    def get_queryset(self):
        """

        :return:
        """
        return None

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('airquality:index'))
