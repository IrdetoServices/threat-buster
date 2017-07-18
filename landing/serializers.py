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

from rest_framework import serializers

from landing.models import ParentCategory, ChildCategory, Question, Survey, Tenant, SurveyResult, SurveyResults


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
        fields = ['pk', 'question', 'category', ]


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['pk', 'title', 'question_set']


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name']


class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = ['pk', 'question', 'answer']


class SurveyResultsSerializer(serializers.ModelSerializer):
    survey_results = SurveyResultSerializer(many=True, source='surveyresult_set')

    def create(self, validated_data):
        results = validated_data.pop('surveyresult_set')
        survey_results = SurveyResults.objects.create(**validated_data)
        for result in results:
            SurveyResult.objects.create(survey_results=survey_results, **result)
        return survey_results

    class Meta:
        model = SurveyResults
        fields = ['pk', 'date', 'tenant', 'survey', 'survey_results']
