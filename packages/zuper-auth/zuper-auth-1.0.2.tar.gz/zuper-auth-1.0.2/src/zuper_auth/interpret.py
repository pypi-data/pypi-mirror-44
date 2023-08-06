from collections import defaultdict
from dataclasses import dataclass, field
from typing import *

from zuper_auth.parsing import Statement, NewOType, NewParentRelation, NewAbility, NewObject, SetChildParentRelation, \
    ResourceMatch, ByPattern, Allow, NewProperty, SetProperty, SingleResourceMatch, ConditionMatch, \
    AttributeMatch, Always, AbilityMatch, AbilityMatchByPattern, parse_string, QueryIS, QueryHAS, QueryGetProperties, \
    AndMatch, HasAttributes
from zuper_commons.text.zc_wildcards import wildcard_to_regexp


@dataclass
class Object:
    main_name: str
    others: List[str]
    type_name: str
    parents: Dict[str, 'Object'] = field(default_factory=dict)
    children: Dict[str, 'Object'] = field(default_factory=dict)
    properties: Dict[str, List[ResourceMatch]] = field(default_factory=lambda: defaultdict(list))


@dataclass
class OType:
    t_parents: Dict[str, bool] = field(default_factory=dict)
    t_abilities: Dict[str, str] = field(default_factory=dict)
    t_objects: Dict[str, Object] = field(default_factory=dict)
    t_properties: Dict[str, str] = field(default_factory=dict)


class AuthException(Exception):
    pass


class Invalid(AuthException):
    pass


class CouldNotFindResource(AuthException):
    pass


@dataclass
class QResult:
    ok: bool
    line: str
    query_result: Any
    msg: Optional[str]


class Interpreter:
    types: Dict[str, OType]
    allows: List[Allow]

    statements_history: List[Statement]
    results: List[QResult]

    def __init__(self):
        self.types = {}
        self.allows = []
        self.statements_history = []
        self.results = []
        self.results_history = []
        self.last_line = None

    def interpret(self, line: str, statement: Statement):
        self.last_line = line
        self.statements_history.append(statement)
        t = type(statement).__name__
        f = f'interpret_{t}'
        if not hasattr(self, f):
            msg = f'Cannot find {f}'
            raise NotImplementedError(msg)

        ff = getattr(self, f)
        try:
            ff(statement)
        except AuthException as e:
            self._mark_failure(str(e))
        except BaseException as e:
            msg = f'Cannot intepret statement {statement}'
            raise ValueError(msg) from e

    def _mark_ok(self, msg=None):
        qr = QResult(ok=True, msg=msg, line=self.last_line, query_result=None)
        self.results.append(qr)
        self.results_history.append(qr)

    def _mark_failure(self, msg):
        qr = QResult(ok=False, msg=msg, line=self.last_line, query_result=None)
        self.results.append(qr)
        self.results_history.append(qr)

    def _mark_query_result(self, res, msg=None):
        qr = QResult(ok=True, msg=msg, line=self.last_line, query_result=res)
        self.results.append(qr)
        self.results_history.append(qr)

    def get_results(self) -> List[QResult]:
        r = self.results
        self.results = []
        return r

    def _get_type(self, type_name):
        if type_name not in self.types:
            msg = f'Could not find type {type_name!r}'
            raise Invalid(msg)
        return self.types[type_name]

    def interpret_NewOType(self, s: NewOType):
        if s.type_name in self.types:
            msg = f'Already know find type {s.type_name!r}'
            raise Invalid(msg)
        self.types[s.type_name] = OType()
        self._mark_ok()

    def interpret_NewParentRelation(self, s: NewParentRelation):
        t = self._get_type(s.type_name)
        if s.parent_name in t.t_parents:
            msg = f'Already set relationship.'
            raise Invalid(msg)

        t.t_parents[s.parent_name] = s.compulsory
        self._mark_ok()

    def interpret_NewAbility(self, s: NewAbility):
        t = self._get_type(s.type_name)
        if s.ability_name in t.t_abilities:
            msg = f'Already set ability {s.ability_name!r}.'
            raise Invalid(msg)
        t.t_abilities[s.ability_name] = s.title
        self._mark_ok()

    def interpret_NewObject(self, s: NewObject):
        t = self._get_type(s.type_name)
        main_name = s.identifiers[0]
        others = s.identifiers[1:]
        if main_name in t.t_objects:
            msg = f'Already know object {main_name!r}.'
            raise Invalid(msg)
        t.t_objects[main_name] = Object(main_name=main_name, others=others, type_name=s.type_name)
        self._mark_ok()

    def interpret_SetChildParentRelation(self, s: SetChildParentRelation):
        for parent in self.get_resources(s.parent_match):
            for child in self.get_resources(s.child_match):
                # make sure no recursion
                p = list(get_parents_and_self(parent))
                if child in p:
                    msg = f'Cannot set parent-relation because child is a parent of parent.' \
                        f'\nParent: {parent}' \
                        f'\nChild: {child}' \
                        f'\ns: {s}'
                    raise Invalid(msg)

                child.parents[parent.main_name] = parent
                parent.children[child.main_name] = child
        self._mark_ok()

    def interpret_NewProperty(self, s: NewProperty):
        t = self._get_type(s.type_name)
        if s.property_name in t.t_properties:
            msg = f'Already set property {s.property_name!r}.'
            raise Invalid(msg)
        t.t_properties[s.property_name] = s.title
        self._mark_ok()

    def interpret_SetProperty(self, s: SetProperty):
        for r in self.get_resources(s.resource_match):
            t = self.types[r.type_name]
            if s.property_name not in t.t_properties:
                msg = f'Cannot set property {s.property_name!r} for object {r.main_name!r} of type {r.type_name!r}.'
                raise Invalid(msg)
            r.properties[s.property_name].append(s.context)
        self._mark_ok()

    def interpret_Allow(self, s: Allow):
        self.allows.append(s)
        self._mark_ok()

    def get_resources(self, rm: ResourceMatch) -> Iterator[Object]:
        if isinstance(rm, ByPattern):
            t = self._get_type(rm.type_name)
            for obname, ob in list(t.t_objects.items()):
                for identifier in [ob.main_name] + ob.others:
                    if pattern_matches(rm.pattern, identifier):
                        yield ob
            return

        raise NotImplementedError(rm)

    def get_resource(self, rm: SingleResourceMatch) -> Object:
        t = self.types[rm.type_name]
        for obname, ob in list(t.t_objects.items()):
            for identifier in [ob.main_name] + ob.others:
                if rm.identifier == identifier:
                    return ob
        msg = f'Could not find resource corresponding to {rm}'
        raise CouldNotFindResource(msg)

    def interpret_QueryIS(self, query: QueryIS):
        # logger.debug(f'query {query}')
        user = self.get_resource(query.user)
        context = self.get_resource(query.context)
        t = self._get_type(context.type_name)
        ability = query.ability
        if not ability in t.t_abilities:
            msg = f'Unknown ability {ability!r} for object of type {context.type_name!r}.'
            msg += f'\nKnown: {",".join(t.t_abilities)}.'
            raise Invalid(msg)

        properties = get_active_properties(user, context)
        # logger.info('properties: %s' % properties)
        context_parents = list(get_parents_and_self(context))
        user_parents = list(get_parents_and_self(user))

        msg = 'Active properties: %s' % properties
        msg += f'\nuser hierarchy:'
        for p in user_parents:
            msg += f'\n - {p.type_name} : {p.main_name}'
        msg += f'\nresource hierarchy: '
        for p in context_parents:
            msg += f'\n - {p.type_name} : {p.main_name}'
        for allow in self.allows:
            c1 = any(rmatch(allow.user_match, _) for _ in user_parents)
            c2 = amatch(allow.ability_match, ability)
            c3 = any(rmatch(allow.context_match, _) for _ in context_parents)
            c4 = cmatch(allow.condition, properties)
            ok = c1 and c2 and c3 and c4

            if ok:
                self._mark_query_result(True)
                return
            else:
                pass
                msg += f'\nfalse (user match {c1}, amatch {c2}, context match {c3}, condition match{c4})\n for {allow}'

        self._mark_query_result(False, msg)

    def interpret_QueryHAS(self, query: QueryHAS):
        # logger.debug(f'query {query}')
        user = self.get_resource(query.user)
        context = self.get_resource(query.context)

        properties = get_active_properties(user, context)
        # logger.debug('properties: %s' % properties)
        res = query.property in properties
        self._mark_query_result(res)

    def interpret_QueryGetProperties(self, query: QueryGetProperties):
        user = self.get_resource(query.user)
        context = self.get_resource(query.context)

        properties = get_active_properties(user, context)

        self._mark_query_result(properties)

    def parse_and_interpret(self, src: str):
        for line, statement in parse_string(src):
            self.interpret(line, statement)

    def get_history(self) -> str:
        res = []
        for s in self.results_history:
            res.append(str(s))
        return "\n".join(res)


def amatch(am: AbilityMatch, ability):
    if isinstance(am, AbilityMatchByPattern):
        if pattern_matches(am.pattern, ability):
            return True
        return False
    else:
        raise NotImplementedError(am)


def cmatch(cm: ConditionMatch, properties: Dict[str, bool]):
    if isinstance(cm, Always):
        return True

    if isinstance(cm, AttributeMatch):
        for p, v in properties.items():
            if v and pattern_matches(cm.pattern, p):
                return True

        return False
    raise NotImplementedError(cm)


def get_active_properties(user: Object, context: Object):
    user_parents = list(get_parents_and_self(user))
    context_parents = list(get_parents_and_self(context))

    properties = {}

    # Now set the properties
    for cp in context_parents:
        for up in user_parents:
            for pname, matches in up.properties.items():
                for match in matches:
                    if rmatch(match, cp):
                        properties[pname] = True
    return properties


def get_parents_and_self(ob: Object) -> Iterator[Object]:
    for parent in ob.parents.values():
        yield from get_parents_and_self(parent)
    yield ob


def rmatch(rm: ResourceMatch, ob: Object):
    if isinstance(rm, ByPattern):
        if rm.type_name != ob.type_name:
            return False
        for identifier in [ob.main_name] + ob.others:
            if pattern_matches(rm.pattern, identifier):
                return True
        return False
    elif isinstance(rm, AndMatch):
        matches = (rmatch(_, ob) for _ in rm.ops)
        return all(matches)
    elif isinstance(rm, HasAttributes):
        # XXX
        matches = (_ in ob.properties for _ in rm.attributes)
        return all(matches)
    else:
        raise NotImplementedError(rm)


def pattern_matches(pattern, identifier):
    regexp = wildcard_to_regexp(pattern)

    return regexp.match(identifier)
