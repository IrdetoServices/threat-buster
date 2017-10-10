from rest_framework.utils.serializer_helpers import BindingDict

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

class NamedSerializer(serializers.Serializer):
    description = serializers.CharField()
    uid = serializers.CharField()
    title = serializers.CharField()


class AttackerSerializer(NamedSerializer):
    pass


class MitigationSerializer(NamedSerializer):
    pass


class BasicEventSerializer(NamedSerializer):
    pass


class AttackMethodSerializer(NamedSerializer):

    # This is to allow the nested tree of Attack Methods - static defn doesn't work due to N depth of tree.
    @property
    def fields(self):
        """
        A dictionary of {field_name: field_instance}.
        """
        # `fields` is evaluated lazily. We do this to ensure that we don't
        # have issues importing modules that use ModelSerializers as fields,
        # even if Django's app-loading stage has not yet run.
        if not hasattr(self, '_fields'):
            self._fields = BindingDict(self)
            for key, value in self.get_fields().items():
                self._fields[key] = value
            self._fields['attack_methods'] = AttackMethodSerializer(many=True)
        return self._fields

    mitigations = MitigationSerializer(many=True)
    basic_events = BasicEventSerializer(many=True)


class AbstractAttackTreeNodeSerializer(NamedSerializer):
    mitigations = MitigationSerializer(many=True)
    basic_events = BasicEventSerializer(many=True)
    attack_methods = AttackMethodSerializer(many=True)


class AttackGoalSerializer(AbstractAttackTreeNodeSerializer):
    description = serializers.CharField()
    uid = serializers.CharField()
    title = serializers.CharField()

    attackers = AttackerSerializer(many=True)
