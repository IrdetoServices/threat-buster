from django.contrib.auth.models import User
from django.test import TestCase
from guardian.core import ObjectPermissionChecker

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


class CategoryTestCase(TestCase):
    def setUp(self):
        self.parent = ParentCategory.objects.create(category="First Category")
        ChildCategory.objects.create(category="Child1", parent_category=self.parent)
        ChildCategory.objects.create(category="Child2", parent_category=self.parent)

    def test_counting(self):
        parent = ParentCategory.objects.get(pk=self.parent.id)
        self.assertEquals(2, parent.category_count())

    def test_summary(self):
        parent = ParentCategory.objects.get(pk=self.parent.id)
        self.assertEquals("Child1, Child2", parent.category_list())


class DataLoadTestCase(TestCase):
    fixtures = ['10_create_categories', '20_questions.json']

    def testDataLoaded(self):
        self.assertGreater(ParentCategory.objects.count(), 0)
        self.assertGreater(Survey.objects.count(), 0)
        self.assertGreater(Question.objects.count(), 0)


class TenantGroupsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')

    def testTenantCreation(self):
        tenant = Tenant.objects.create(name='tenant')
        tenant.save()
        tenant_loaded = Tenant.objects.filter(pk=tenant.pk)
        self.assertIsNotNone(tenant_loaded)
        self.assertEquals(tenant.name, "tenant")
        self.assertIsNotNone(tenant.group)
        self.assertEquals(tenant.group.name, "TenantGroup{}".format(tenant.pk))
        self.assertTrue(ObjectPermissionChecker(tenant.group).has_perm('view_tenant', tenant))
        self.assertTrue(ObjectPermissionChecker(tenant.group).has_perm('change_tenant', tenant))

    def testTenantAddingUserOnCreation(self):
        tenant = Tenant.objects.create(name='tenantAddingUsers')
        tenant.users.add(self.user1)
        tenant.save()

        tenant_loaded = Tenant.objects.filter(pk=tenant.pk)
        self.assertIsNotNone(tenant_loaded)
        self.assertEquals(tenant.name, "tenantAddingUsers")
        self.assertIsNotNone(tenant.group)
        self.assertIsNotNone(tenant.users)
        self.assertTrue(self.user1.groups.filter(pk=tenant.group.pk).exists())
        self.assertTrue(tenant.users.filter(pk=self.user1.pk).exists())
        self.assertTrue(ObjectPermissionChecker(tenant.group).has_perm('view_tenant', tenant))

    def testTenantAddingUserAfterCreation(self):
        tenant = Tenant.objects.create(name='tenantAddingUsers')
        tenant.save()
        self.assertFalse(self.user1.has_perm('view_tenant', tenant))
        tenant.users.add(self.user1)
        tenant.save()
        self.assertTrue(self.user1.has_perm('view_tenant', tenant))

        tenant_loaded = Tenant.objects.filter(pk=tenant.pk)
        self.assertIsNotNone(tenant_loaded)
        self.assertEquals(tenant.name, "tenantAddingUsers")
        self.assertIsNotNone(tenant.group)
        self.assertIsNotNone(tenant.users)
        self.assertTrue(self.user1.groups.filter(pk=tenant.group.pk).exists())
        self.assertTrue(tenant.users.filter(pk=self.user1.pk).exists())
        self.assertTrue(ObjectPermissionChecker(tenant.group).has_perm('view_tenant', tenant))

    def testTenantRemovingUsers(self):
        tenant = Tenant.objects.create(name='tenantRemovingUsers')
        tenant.users.add(self.user1)
        tenant.users.add(self.user2)
        tenant.save()

        tenant_loaded = Tenant.objects.filter(pk=tenant.pk)
        self.assertIsNotNone(tenant_loaded)
        self.assertEquals(tenant.name, "tenantRemovingUsers")
        self.assertIsNotNone(tenant.group)
        self.assertIsNotNone(tenant.users)
        self.assertTrue(self.user1.groups.filter(pk=tenant.group.pk).exists())
        self.assertTrue(tenant.users.filter(pk=self.user1.pk).exists())
        self.assertTrue(tenant.users.filter(pk=self.user2.pk).exists())

        tenant.users.remove(self.user2)
        tenant.save()

        self.assertTrue(self.user1.groups.filter(pk=tenant.group.pk).exists())
        self.assertTrue(self.user1.has_perm('view_tenant', tenant))
        self.assertFalse(self.user2.groups.filter(pk=tenant.group.pk).exists())
        self.assertFalse(self.user2.has_perm('view_tenant', tenant))

        self.assertTrue(tenant.users.filter(pk=self.user1.pk).exists())
        self.assertFalse(tenant.users.filter(pk=self.user2.pk).exists())
