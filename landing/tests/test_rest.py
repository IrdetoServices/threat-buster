from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase
from six import BytesIO

from landing.models import ParentCategory, ChildCategory, Survey, Question, Tenant

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
        stream = BytesIO(response.content)
        responseSurvey = JSONParser().parse(stream)
        self.assertIsNotNone(responseSurvey)
        self.assertEquals(responseSurvey['title'], self.survey.title)
        self.assertEquals(responseSurvey['question_set'][0]['question'], "Question 1")


class TenantPermsTestCase(APITestCase):
    def setUp(self):
        self.tenant1 = Tenant.objects.create(name="Tenant Test Case 1")
        self.tenant2 = Tenant.objects.create(name="Tenant Test Case 2")
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.tenant1.users.add(self.user1)
        self.tenant2.users.add(self.user2)
        self.tenant1.save()
        self.tenant2.save()

    def testVerifyRead(self):
        reponse_user1 = self.loadTenants(self.user1)
        self.assertEquals(len(reponse_user1), 1)
        self.assertEquals(reponse_user1[0]['name'], "Tenant Test Case 1")

        response_user2 = self.loadTenants(self.user2)
        self.assertEquals(len(response_user2), 1)
        self.assertEquals(response_user2[0]['name'], "Tenant Test Case 2")

        response_user1_tenant1 = self.loadTenant(self.user1, self.tenant1.id)
        self.assertEquals(response_user1_tenant1['name'], "Tenant Test Case 1")

        response_user2_tenant1 = self.loadTenant(self.user2, self.tenant1.id)
        self.assertEquals(response_user2_tenant1['detail'], "Not found.")

    def testVerifyWrite(self):
        response_user1_tenant1 = self.loadTenant(self.user1, self.tenant1.id)
        response_user1_tenant1['name'] = "bob"
        self.client.force_authenticate(user=self.user1)
        post_response = self.client.put("/api/tenants/{}/".format(self.tenant1.id), response_user1_tenant1)
        self.assertEquals(post_response.status_code, 200)
        tenant_reload = Tenant.objects.get(id=self.tenant1.id)
        self.assertEquals(tenant_reload.name, "bob")

        self.client.force_authenticate(user=self.user2)
        response_user1_tenant1['name'] = "bob1"
        post_response = self.client.put("/api/tenants/{}/".format(self.tenant1.id), response_user1_tenant1)
        self.assertEquals(post_response.status_code, 404)
        tenant_reload = Tenant.objects.get(id=self.tenant1.id)
        self.assertEquals(tenant_reload.name, "bob")

    def testVerifyCreate(self):
        newTenant = {"name": 'bobbins'}
        self.client.force_login(self.user1)
        post_response = self.client.post("/api/tenants/", newTenant)
        self.assertEquals(post_response.status_code, 403)

    def loadTenant(self, user, id):
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/tenants/{}/".format(id))
        stream = BytesIO(response.content)
        return JSONParser().parse(stream)

    def loadTenants(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/tenants/')
        stream = BytesIO(response.content)
        return JSONParser().parse(stream)


class QuestionRestTestCase(APITestCase):
    def setUp(self):
        self.tenant1 = Tenant.objects.create(name="Tenant Test Case 1")
        self.tenant2 = Tenant.objects.create(name="Tenant Test Case 2")
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.tenant1.users.add(self.user1)
        self.tenant2.users.add(self.user2)
        self.tenant1.save()
        self.tenant2.save()
        self.parent = ParentCategory.objects.create(category="First Category")
        child1 = ChildCategory.objects.create(category="Child1", parent_category=self.parent)
        child2 = ChildCategory.objects.create(category="Child2", parent_category=self.parent)
        self.survey = Survey.objects.create(title="Test")
        Question.objects.create(question="Question 1", category=child1, survey=self.survey)
        Question.objects.create(question="Question 2", category=child2, survey=self.survey)

    def testSurveyCompletion(self):
        self.client.force_login(self.user1)
        post = {"date": "2017-07-18",
                "tenant": self.tenant1.id,
                "survey": self.survey.id,
                "survey_results": []}

        response = self.client.post("/api/survey_results/", post)
        self.assertEquals(response.status_code, 201)

        self.client.force_login(self.user2)
        response2 = self.client.post("/api/survey_results/", post)
        self.assertEquals(response2.status_code, 403)
