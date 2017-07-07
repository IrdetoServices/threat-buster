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

from django.contrib import admin

# Register your models here.
from .models import Tenant, Survey, Question, ParentCategory, ChildCategory


class UsersInLine(admin.TabularInline):
    model = Tenant.users.through
    extra = 3
    can_delete = False


class TenantAdmin(admin.ModelAdmin):
    fields = ['name', 'active']
    inlines = [UsersInLine]
    list_display = ('name', 'active')
    list_filter = ['active']
    search_fields = ['name']


class QuestionsInLine(admin.TabularInline):
    model = Question
    fields = ['question', 'category', 'order']
    list_display = ['question', 'category', 'order']

class ChildCategoryInLine(admin.TabularInline):
    model = ChildCategory


@admin.register(ParentCategory)
class ParentAdmin(admin.ModelAdmin):
    inlines = [ChildCategoryInLine]
    fields = ['category']
    list_display = ['category', 'order', 'category_list']
    list_editable = ['order']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    fields = ['title']
    inlines = [QuestionsInLine]


admin.site.register(Tenant, TenantAdmin)
