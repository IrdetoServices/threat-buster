import landing
from landing.graph_models import Tenant, AttackGoal, AttackMethod, BasicEvent, Mitigation, Attacker
from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    def handle(self, *args, **options):
        tenant_db = landing.models.Tenant.objects.create(name='tenant')
        tenant_db.save()

        tenant = Tenant(tenant='tenant').save()
        attack_goal = AttackGoal(title="Steal Lawnmower", attack_cost=1000, impact_attack_cost=5000).save()
        tenant.attack_trees.connect(attack_goal)
        attack_method_1 = AttackMethod(title="Break Into Storage", goal_rules="A").save()
        attack_goal.attack_methods.connect(attack_method_1)
        attack_method_2 = AttackMethod(title="Steal from Operator", goal_rules="O").save()
        attack_goal.attack_methods.connect(attack_method_2)

        basic_event_1 = BasicEvent(title="Break open door", attack_cost=10, technical_skill=30).save()
        attack_method_1.basic_events.connect(basic_event_1)
        mitigation_1 = Mitigation(title="Padlock", attack_cost=50, technical_skill=50).save()
        attack_method_1.mitigations.connect(mitigation_1)

        basic_event_2 = BasicEvent(title="Hold up at gunpoint", attack_cost=500, technical_skill=20).save()
        attack_method_2.basic_events.connect(basic_event_2)
        mitigation_2 = Mitigation(title="Guard Dog", attack_cost=1000, technical_skill=80).save()
        attack_method_2.mitigations.connect(mitigation_2)

        attack_method_3 = AttackMethod(title="Many options method", goal_rules="O").save()
        attack_goal.attack_methods.connect(attack_method_3)

        attack_method_3a = AttackMethod(title="Many options method a", goal_rules="A").save()
        attack_method_3.attack_methods.connect(attack_method_3a)

        basic_event_3a = BasicEvent(title="Event 3a", attack_cost=10, technical_skill=30).save()
        attack_method_3a.basic_events.connect(basic_event_3a)
        mitigation_3a = Mitigation(title="Mitigation 3a", attack_cost=50, technical_skill=50).save()
        attack_method_3a.mitigations.connect(mitigation_3a)

        attack_method_3b = AttackMethod(title="Many options method b", goal_rules="A").save()
        attack_method_3.attack_methods.connect(attack_method_3b)

        basic_event_3b = BasicEvent(title="Event 3a", attack_cost=10, technical_skill=30).save()
        attack_method_3b.basic_events.connect(basic_event_3b)
        mitigation_3b = Mitigation(title="Mitigation 3a", attack_cost=50, technical_skill=50).save()
        attack_method_3b.mitigations.connect(mitigation_3b)

        attacker_strong = Attacker(title="Mafia", attack_cost=1000, technical_skill=80).save()
        attack_goal.attackers.connect(attacker_strong)

        attacker_weak = Attacker(title="Chancer", attack_cost=5, technical_skill=10).save()
        attack_goal.attackers.connect(attacker_weak)
