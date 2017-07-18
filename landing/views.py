from rest_framework import viewsets, filters

from landing.filters import TenantFilter, TenantPermission
from landing.models import Survey, Tenant, SurveyResults
from landing.serializers import SurveySerializer, TenantSerializer, SurveyResultsSerializer

__copyright__ = """

    Copyright 2017 Irdeto BV

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'landing/index.html')


@login_required
def profile(request):
    user_tenants = request.user.tenant_set.all()
    context = {
        'user_tenants': user_tenants
    }
    return render(request, 'landing/profile.html')


class Dashboard(TemplateView):
    template_name = "landing/profile_dashboard.html"

    def get_context_data(self, **kwargs):
        xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi",
                 "Lemon"]
        ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
        chartdata = {'x': xdata, 'y': ydata}
        charttype = "pieChart"
        chartcontainer = 'piechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return data


class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    filter_backends = (filters.DjangoObjectPermissionsFilter,)


class SurveyResultsViewSet(viewsets.ModelViewSet):
    queryset = SurveyResults.objects.all()
    serializer_class = SurveyResultsSerializer

    filter_backends = (TenantFilter,)
    permission_classes = (TenantPermission,)
