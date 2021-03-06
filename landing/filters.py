from rest_framework import permissions

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

from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import BasePermission, DjangoObjectPermissions


class TenantFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user

        if not user.is_superuser:
            queryset = queryset.filter(tenant=user.tenant_set.all())

        return queryset

class TenantPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_superuser:
            return user.tenant_set.exists(tenant=obj.tenent)
        else:
            return True

    def has_permission(self, request, view):
        user = request.user

        if not user.is_superuser:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                # should have a tenant in the request body
                assert (request.data['tenant'])
                return user.tenant_set.filter(pk=request.data['tenant']).exists()
        else:
            return True


class UpdatableObjectPermission(DjangoObjectPermissions):
    # This class 'fixes' behaviour on the default object which doesn't seem to work well with Django-Guardian. Namely
    # the default class assumes users will have change permission on the model as well as the object permission. This is
    # not true in Django Guardian by default. Returning True does not introduce security issue as security is enforced by
    # the object level check later.

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PUT', 'PATCH'):
            return True

        return super(UpdatableObjectPermission, self).has_permission(request, view)
