from landing.models import Survey, Question, ChildCategory, ParentCategory

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

from django.conf.urls import url, include

from landing.views import *
from . import views
from rest_framework import routers, serializers, viewsets


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = ["pk", "category"]


class ChildCategorySerializer(serializers.ModelSerializer):
    parent_category = ParentCategorySerializer()

    class Meta:
        model = ChildCategory
        fields = ["pk", "category", "parent_category"]


class QuestionSerializer(serializers.ModelSerializer):
    category = ChildCategorySerializer()

    class Meta:
        model = Question
        fields = ['question', 'category', ]


# Serializers define the API representation.
class SurveySerializer(serializers.HyperlinkedModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['title', 'question_set']


# ViewSets define the view behavior.
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


router = routers.DefaultRouter()
router.register(r'surveys', SurveyViewSet)

app_name = 'landing'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^accounts/profile/$", views.profile, name='profile'),
    url(r"^accounts/profile/dashboard/$", Dashboard.as_view(), name='dashboard'),
    url(r'^api/', include(router.urls))]
