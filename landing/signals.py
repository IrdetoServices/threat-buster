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

import logging

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm

from landing.models import Tenant

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Tenant)
def tenant_callback(sender, instance, **kwargs):
    logger.debug("Tenant saved: {instance}".format(instance=instance))

    if instance.group is None:
        # Create group for Tenant
        instance.group = Group.objects.create(name="TenantGroup{}".format(instance.pk))

    checker = ObjectPermissionChecker(instance.group)
    if not checker.has_perm('view_tenant', instance):
        assign_perm('view_tenant', instance.group, instance)
    if not checker.has_perm('change_tenant', instance):
        assign_perm('change_tenant', instance.group, instance)

    # sync users in group with current list
    usersInGroup = User.objects.filter(groups=instance.group)
    usersToRemove = set(usersInGroup).difference(set(instance.users.all()))
    usersToAdd = set(instance.users.all()).difference(set(usersInGroup))

    logger.debug("Removing: {}, Adding {}".format(usersToRemove, usersToAdd))

    for user in usersToRemove:
        user.groups.remove(instance.group)
    usersToRemove.update()

    for user in usersToAdd:
        user.groups.add(instance.group)
    usersToAdd.update()

    logger.debug("Removed: {}, Added {}".format(usersToRemove, usersToAdd))