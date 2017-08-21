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

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            username = os.environ['SUPER_USER_NAME']
            email_ = os.environ['SUPER_USER_EMAIL']
            password_ = os.environ['SUPER_USER_PASSWORD']
        except KeyError:
            self.stdout.write(self.style.WARNING('SUPER_USER_[USERNAME|EMAIL|PASSWORD is not set. \n %s' % os.environ))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username,
                                          email_,
                                          password_)
