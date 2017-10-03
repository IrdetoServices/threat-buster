from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom)


class AbstractAttackTreeNode(StructuredNode):
    __abstract_node__ = True

    title = StringProperty(required=True)
    description = StringProperty(required=False)
    uid = UniqueIdProperty()

    basic_events = RelationshipTo('BasicEvent', "EVENT")
    attack_methods = RelationshipTo('AttackMethod', "METHOD")
    mitigations = RelationshipTo('Mitigation', "MITIGATION")


class TechnicalSkillMixin(object):
    # The technical skill associated with this node
    technical_skill = IntegerProperty()


class MonetaryMixin(object):
    # The cost associated with this node.
    cost = IntegerProperty()


class BasicEvent(AbstractAttackTreeNode, TechnicalSkillMixin, MonetaryMixin):
    pass


class AttackMethod(AbstractAttackTreeNode, TechnicalSkillMixin, MonetaryMixin):
    GOAL_RULES = (
        ('A', "And"),
        ('O', "Or")
    )
    # Goal rules define if child nodes are combined in AND or OR fashion
    goal_rules = StringProperty(required=True, choices=GOAL_RULES)


class AttackGoal(AbstractAttackTreeNode, MonetaryMixin):
    # Monetary cost to the defender for the attack per sucessful attack (not the same as the
    # reward to attacker for performing the attack)
    monetary_cost = IntegerProperty()
    attackers = RelationshipTo('Attacker', "ATTACKERS")


class Mitigation(AbstractAttackTreeNode, TechnicalSkillMixin, MonetaryMixin):
    pass


class Attacker(StructuredNode, MonetaryMixin):
    title = StringProperty(required=True)
    description = StringProperty(required=False)
    uid = UniqueIdProperty()


# Represents a Tenants graphs
class Tenant(StructuredNode):
    tenant = StringProperty(required=True, unique=True)
    attack_trees = RelationshipTo(AttackGoal, 'ATTACK_TREE')
