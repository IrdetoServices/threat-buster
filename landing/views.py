import json

from django.utils.decorators import method_decorator
from neomodel import db
from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from landing.filters import TenantFilter, TenantPermission, UpdatableObjectPermission, AttackGoalFilter
from landing.graph_models import AttackGoal
from landing.models import Survey, Tenant, SurveyResults
from landing.serializers import SurveySerializer, TenantSerializer, SurveyResultsSerializer, AttackGoalSerializer

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
from django.shortcuts import render, get_object_or_404
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class AttackGoals(TemplateView):
    template_name = "landing/attack_goals.html"


class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    permission_classes = (UpdatableObjectPermission,)


class SurveyResultsViewSet(viewsets.ModelViewSet):
    queryset = SurveyResults.objects.all()
    serializer_class = SurveyResultsSerializer

    filter_backends = (TenantFilter,)
    permission_classes = (TenantPermission,)


class AttackGoalViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = AttackGoalSerializer
    filter_backends = (AttackGoalFilter,)

    def get_queryset(self):
        return AttackGoal.nodes

    def retrieve(self, request, pk=None):
        node = AttackGoal.nodes.get(pk)
        serializer = AttackGoalSerializer(node)
        return Response(serializer.data)


class AttackTreeGraphson(viewsets.ViewSet):
    def list(self, request):
        relations, nodesMeta = db.cypher_query("MATCH (a:AttackGoal)-[b*]->(c) return a,b,c", None)

        outputNodes = []
        outputEdges = []

        outputNodes.append({
            "id": len(outputNodes),
            "uid": relations[0][0].id,
            "caption": relations[0][0].properties['title'],
            "type": list(relations[0][0].labels)[0],
            "root": True
        })

        ids = {relations[0][0].id: len(outputNodes) - 1}

        for relation in relations:
            outputNodes.append({
                "id": len(outputNodes),
                "uid": relation[2].id,
                "caption": relation[2].properties['title'],
                "type": list(relation[2].labels)[0]
            })
            ids[relation[2].id] = len(outputNodes) - 1

            for relationship in relation[1]:
                outputEdges.append({
                    "source": ids[relationship.start],
                    "target": ids[relationship.end],
                    "type": relationship.type

                })

        return Response({'nodes': outputNodes, 'edges': outputEdges})
