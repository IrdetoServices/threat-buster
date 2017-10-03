from uuid import uuid4

from django.test import TestCase
from neomodel import db, clear_neo4j_database

from landing.graph_models import AttackGoal, AttackMethod, Mitigation, BasicEvent, Tenant

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


class GraphTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant(tenant='tests{}'.format(uuid4().urn)).save()

    def tearDown(self):
        results, meta = db.cypher_query(
            "MATCH (n:Tenant)-[*]->(m) WHERE n.tenant={tenant} DETACH delete (m) DETACH DELETE (n)",
            params={'tenant': self.tenant.tenant})
        self.assertIsNotNone(results)

    def test_assembling_attack_tree(self):
        attack_goal = AttackGoal(title="Steal Lawnmower").save()
        self.assertIsNotNone(attack_goal)
        self.tenant.attack_trees.connect(attack_goal)

        attack_method_1 = AttackMethod(title="Break Into Storage", goal_rules="A").save()
        attack_goal.attack_methods.connect(attack_method_1)
        attack_method_2 = AttackMethod(title="Steal from Operator", goal_rules="O").save()
        attack_goal.attack_methods.connect(attack_method_2)

        basic_event_1 = BasicEvent(title="Break open door").save()
        attack_method_1.basic_events.connect(basic_event_1)
        mitigation_1 = Mitigation(title="Padlock").save()
        attack_method_1.mitigations.connect(mitigation_1)

        basic_event_2 = BasicEvent(title="Hold up at gunpoint").save()
        attack_method_2.basic_events.connect(basic_event_2)
        mitigation_2 = Mitigation(title="Guard Dog").save()
        attack_method_2.mitigations.connect(mitigation_2)

        # Results as strings
        results, meta = db.cypher_query(
            "MATCH (a:Tenant)-[r*]->(b) WHERE a.tenant={tenant} RETURN (b.title), reduce (s=\"\", x in r | s+type(x)+',' )",
            params={'tenant': self.tenant.tenant})
        self.assertIsNotNone(results)
        self.assertEqual(7, len(results))
        self.assertTrue(['Steal Lawnmower', 'ATTACK_TREE,'] in results)

        # Results at object level
        results2, meta = db.cypher_query(
            "MATCH (a:Tenant)-[r*]->(b) WHERE a.tenant={tenant} RETURN (b.title), r",
            params={'tenant': self.tenant.tenant})
        self.assertIsNotNone(results2)
        self.assertEqual(7, len(results2))
