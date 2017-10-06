from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom, One)


class NamingMixin(object):
    title = StringProperty(required=True)
    description = StringProperty(required=False)
    uid = UniqueIdProperty()


class AbstractAttackTreeNode(StructuredNode, NamingMixin):
    __abstract_node__ = True

    basic_events = RelationshipTo('BasicEvent', "EVENT")
    attack_methods = RelationshipTo('AttackMethod', "METHOD")
    mitigations = RelationshipTo('Mitigation', "MITIGATION")


class TechnicalSkillMixin(object):
    # The technical skill associated with this node
    technical_skill = IntegerProperty()


class MonetaryMixin(object):
    # The cost associated with succeeding to attack this node.
    attack_cost = IntegerProperty()


class BasicEvent(StructuredNode, NamingMixin, TechnicalSkillMixin, MonetaryMixin):
    parent = RelationshipTo('AbstractAttackTreeNode', "EVENT", cardinality=One)


class AttackMethod(AbstractAttackTreeNode, TechnicalSkillMixin, MonetaryMixin):
    GOAL_RULES = (
        ('A', "And"),
        ('O', "Or")
    )
    # Goal rules define if child nodes are combined in AND or OR fashion
    goal_rules = StringProperty(required=True, choices=GOAL_RULES)

    parent = RelationshipTo('AbstractAttackTreeNode', "EVENT", cardinality=One)

    def successful_attack(self, attacker):
        if self.goal_rules == 'A':
            technical_skill = 0
            attack_cost = 0

            for attack_method in self.attack_methods:
                if not attack_method.successful_attack(attacker):
                    # Quick exit for AND scenario
                    return False

            for mitigation in self.mitigations:
                attack_cost += mitigation.attack_cost
                technical_skill += mitigation.technical_skill

            for basic_event in self.basic_events:
                attack_cost += basic_event.attack_cost
                technical_skill += basic_event.technical_skill

            if technical_skill < attacker.technical_skill and attack_cost < attacker.attack_cost:
                return True
            else:
                return False
        else:

            for attack_method in self.attack_methods:
                if attack_method.successful_attack(attacker):
                    # Quick exit for OR scenario
                    return True

            for mitigation in self.mitigations:
                if mitigation.technical_skill < attacker.technical_skill and mitigation.attack_cost < attacker.attack_cost:
                    return True

            for basic_event in self.basic_events:
                if basic_event.technical_skill < attacker.technical_skill and basic_event.attack_cost < attacker.attack_cost:
                    return True

            return False



class AttackGoal(AbstractAttackTreeNode, MonetaryMixin):
    # Monetary cost to the defender for the attack per sucessful attack (not the same as the
    # reward to attacker for performing the attack)
    impact_cost = IntegerProperty()
    attackers = RelationshipTo('Attacker', "ATTACKERS")


class Mitigation(StructuredNode, NamingMixin, TechnicalSkillMixin, MonetaryMixin):
    implementation_cost = IntegerProperty()
    parent = RelationshipTo('AbstractAttackTreeNode', "EVENT", cardinality=One)


class Attacker(StructuredNode, NamingMixin, MonetaryMixin):
    target = RelationshipTo('AttackGoal', "ATTACKERS")

    def successful_attack(self):
        query = '''match (goal:AttackGoal) --> (attacker:Attacker) 
                    where id(attacker) = {self} with goal, attacker
                    match (goal) -[:METHOD]-> (attackMethods)
                    return attackMethods'''
        attack_outcome, meta = self.cypher(query)

        for result in attack_outcome:
            attackMethod = AttackMethod.inflate(result[0])
            if attackMethod.successful_attack(self):
                return True

        return False


# Represents a Tenants graphs
class Tenant(StructuredNode):
    tenant = StringProperty(required=True, unique=True)
    attack_trees = RelationshipTo(AttackGoal, 'ATTACK_TREE')
