from django.test import TestCase

from landing.models import Tenant, ParentCategory, ChildCategory, Survey, Question
from landing.serializers import SurveyResultsSerializer

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


class ResultSerializerTestCase(TestCase):
    def setUp(self):
        self.tenant1 = Tenant.objects.create(name="Tenant Test Case 1")
        self.parent = ParentCategory.objects.create(category="First Category")
        child1 = ChildCategory.objects.create(category="Child1", parent_category=self.parent)
        child2 = ChildCategory.objects.create(category="Child2", parent_category=self.parent)
        self.survey = Survey.objects.create(title="Test")
        self.q1 = Question.objects.create(question="Question 1", category=child1, survey=self.survey)
        self.q2 = Question.objects.create(question="Question 2", category=child2, survey=self.survey)

    def testResultSerializer(self):
        data = {"date": "2017-07-18",
                "tenant": self.tenant1.pk,
                "survey": self.survey.pk,
                "survey_results": [{
                    "question": self.q1.pk,
                    "answer": True},
                    {
                        "question": self.q2.pk,
                        "answer": False
                    }]}

        serializer = SurveyResultsSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data['surveyresult_set'][0]['answer'])
        self.assertFalse(serializer.validated_data['surveyresult_set'][1]['answer'])
