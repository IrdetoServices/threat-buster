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

import django_tables2 as tables
from django.utils.html import *
from django_tables2 import A

from landing.models import Tenant


class TenantTable(tables.Table):
    name = tables.LinkColumn('landing:site-details', args=[A('pk')], verbose_name='Site')
    active = tables.Column
    endpoints = tables.Column(empty_values=(), orderable=False)

    def render_endpoints(self, record):
            row = "<ul>"
            for endpoint in record.endpoint_set.all():
                row += format_html("<li> {} </li>", endpoint.endpoint_hostname)
            row += "</ul>"
            return format_html(row)

    class Meta:
        model = Tenant
        sequence = ('name', 'endpoints', 'active')
        exclude = ('id', 'plan')
        template = 'django_tables2/bootstrap.html'
