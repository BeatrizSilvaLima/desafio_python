# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# function to get facts that were added
def get_added(fact):
    _, _, _, isAdded = fact
    return isAdded

# function to get facts that were excluded
def get_excluded(fact):
    _, _, _, isAdded = fact
    if not isAdded:
        return (*fact[0:3], True)

def get_actual(schema, facts):
    dict_schema = dict((attribute, value) for attribute, _, value in schema)

    added = list(filter(get_added, facts))
    excluded = list(filter(None, map(get_excluded,facts)))

    result = {}

    for fact in added:
        if fact not in excluded:
            entity, attribute, value, _ = fact
            if dict_schema[attribute] == 'many':
                result.update({(entity, attribute, value): fact})
            else:
                result.update({(entity, attribute): fact})

    return [*result.values()]

def main():

    facts = [
    ('gabriel', 'endereço', 'av rio branco, 109', True),
    ('joão', 'endereço', 'rua alice, 10', True),
    ('joão', 'endereço', 'rua bob, 88', True),
    ('joão', 'telefone', '234-5678', True),
    ('joão', 'telefone', '91234-5555', True),
    ('joão', 'telefone', '234-5678', False),
    ('gabriel', 'telefone', '98888-1111', True),
    ('gabriel', 'telefone', '56789-1010', True),
    ]

    schema = [
        ('endereço', 'cardinality', 'one'),
        ('telefone', 'cardinality', 'many')
    ]

    result = get_actual(schema, facts)

    expectedResult = [
    ('gabriel', 'endereço', 'av rio branco, 109', True),
    ('joão', 'endereço', 'rua bob, 88', True),
    ('joão', 'telefone', '91234-5555', True),
    ('gabriel', 'telefone', '98888-1111', True),
    ('gabriel', 'telefone', '56789-1010', True)
    ]

    assert result == expectedResult

    print(result)

if __name__ == "__main__":
    main()

# Resultado esperado para este exemplo (mas não precisa ser nessa ordem):
#[
#  ('gabriel', 'endereço', 'av rio branco, 109', True),
#  ('joão', 'endereço', 'rua bob, 88', True),
#  ('joão', 'telefone', '91234-5555', True),
#  ('gabriel', 'telefone', '98888-1111', True),
#  ('gabriel', 'telefone', '56789-1010', True)
#]