from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase

from landing.models import ParentCategory, ChildCategory, Survey, Question

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


# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        self.parent = ParentCategory.objects.create(category="First Category")
        child1 = ChildCategory.objects.create(category="Child1", parent_category=self.parent)
        child2 = ChildCategory.objects.create(category="Child2", parent_category=self.parent)

    def test_counting(self):
        parent = ParentCategory.objects.get(pk=self.parent.id)
        self.assertEquals(2, parent.category_count())

    def test_summary(self):
        parent = ParentCategory.objects.get(pk=self.parent.id)
        self.assertEquals("Child1, Child2", parent.category_list())


class SurveyRestTestCase(APITestCase):
    def setUp(self):
        self.parent = ParentCategory.objects.create(category="First Category")
        child1 = ChildCategory.objects.create(category="Child1", parent_category=self.parent)
        child2 = ChildCategory.objects.create(category="Child2", parent_category=self.parent)

        self.survey = Survey.objects.create(title="Test")
        Question.objects.create(question="Question 1", category=child1, survey=self.survey)
        Question.objects.create(question="Question 2", category=child2, survey=self.survey)

        self.user = User.objects.create(username='api_test')

    def testApi(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/surveys/{id}/'.format(id=self.survey.pk))
        self.assertEquals(response.data,
                          {'title': 'Test', 'question_set': [OrderedDict([('question', 'Question 1'), ('category',
                                                                                                       OrderedDict(
                                                                                                           [('pk', 5), (
                                                                                                               'category',
                                                                                                               'Child1'),
                                                                                                            (
                                                                                                                'parent_category',
                                                                                                                OrderedDict(
                                                                                                                    [(
                                                                                                                        'pk',
                                                                                                                        3),
                                                                                                                        (
                                                                                                                            'category',
                                                                                                                            'First Category')]))]))]),
                                                             OrderedDict([('question', 'Question 2'), ('category',
                                                                                                       OrderedDict(
                                                                                                           [('pk', 6), (
                                                                                                               'category',
                                                                                                               'Child2'),
                                                                                                            (
                                                                                                                'parent_category',
                                                                                                                OrderedDict(
                                                                                                                    [(
                                                                                                                        'pk',
                                                                                                                        3),
                                                                                                                        (
                                                                                                                            'category',
                                                                                                                            'First Category')]))]))])]})
