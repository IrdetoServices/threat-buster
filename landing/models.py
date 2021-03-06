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

from django.contrib.auth.models import User, Group
from django.db import models


# Tenant represents the organization using the service
class Tenant(models.Model):
    name = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User)
    group = models.ForeignKey(Group, blank=True, null=True)

    class Meta:
        verbose_name = "tenant"
        verbose_name_plural = "tenants"

        permissions = (
            ('view_tenant', 'View tenant'),
        )

    def __str__(self):
        return self.name


class Survey(models.Model):
    title = models.TextField(max_length=256)

    def __str__(self):
        return self.title


class Category(models.Model):
    category = models.TextField(max_length=255)
    order = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.category

    class Meta:
        abstract = True
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['order']


class ParentCategory(Category):
    def category_count(self):
        return self.childcategory_set.count()

    def category_list(self):
        return ", ".join(str(value.category) for value in self.childcategory_set.all())


class ChildCategory(Category):
    parent_category = models.ForeignKey(ParentCategory)


class Question(models.Model):
    question = models.TextField(max_length=4096)
    order = models.PositiveIntegerField(default=0, db_index=True)
    survey = models.ForeignKey(Survey)
    category = models.ForeignKey(ChildCategory)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']


class SurveyResults(models.Model):
    date = models.DateField(auto_now=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey)

    def __str__(self):
        return "Results for {} on {}".format(self.tenant, self.date)


class SurveyResult(models.Model):
    question = models.ForeignKey(Question)
    answer = models.BooleanField(blank=False)
    survey_results = models.ForeignKey(SurveyResults)



