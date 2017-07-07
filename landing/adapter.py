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

from allauth.account.adapter import DefaultAccountAdapter

from landing.models import Tenant


class Many2ManyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        super(Many2ManyAccountAdapter, self).save_user(request, user, form, commit)
        tenant = Tenant(name=user.username, active=True)
        # Saved so we can use many-many to add user
        tenant.save()
        tenant.users.add(user)
        user.save()
        tenant.save()
        return user
