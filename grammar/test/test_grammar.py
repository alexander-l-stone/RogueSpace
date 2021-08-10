from grammar.grammar import Grammar
from grammar.rule import Rule
from grammar.grammar import read_grammar
from random import randint

def test_grammar():
    rules = { 'root':Rule('root',["This story is #adj#"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    assert grammar
    assert rules == grammar.rules

def test_missing_root():
    rules = {}
    grammar = Grammar(rules)

    # TODO make sure we have the correct error
    err = "Failed to throw exception"
    try:
        grammar.generate()
    except AttributeError as e:
        err = e.args[0]
    assert "No rule named \"root\" to start from" == err

def test_expansion():
    rules = { 'root':Rule('root',["This story is #adj# #adj#"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert "This story is the best the best" == output

def test_missing_variable():
    rules = { 'root':Rule('root',["This story is #adj# $var$"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)

    # TODO make sure we have the correct error
    err = "Failed to throw exception"
    try:
        grammar.generate()
    except AttributeError as e:
        err = e.args[0]
    assert err.startswith("var not defined before use:")

def test_variable():
    rules = { 'root':Rule('root',["This story is #var:adj# $var$"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert "This story is the best the best" == output

def test_dynamic_rule():
    rules = { 'root':Rule('root',["This story is #var:adj# #$var$#"]), 'adj':Rule('adj',["the best"]), 'the best':Rule("the best",["and dynamic"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert "This story is the best and dynamic" == output

def test_grammar_tag():
    root = Rule('root', ["#tagged<tag>#"])
    rule = Rule('tagged', ["has<tag>", "doesn't have tag"])
    grammar = Grammar({'root':root,'tagged':rule})
    for i in range(10):
        output = grammar.generate()
        assert "has" == output

def test_grammar_multi_tag():
    root = Rule('root', ["#<tag>tagged<other>#"]) # acceptable to invoke tag from anywhere
    rule = Rule('tagged', ["has<tag><other>", "doesn't have other tag<tag>", "doesn't have tag tag<other>"])
    grammar = Grammar({'root':root,'tagged':rule})
    for i in range(10):
        output = grammar.generate()
        assert "has" == output

def test_grammar_tag_root():
    root = Rule('root', ["untagged", "tagged<tag>"])
    grammar = Grammar({'root':root})
    output = grammar.generate('root<tag>')
    assert "tagged" == output

def test_grammar_tag_unclosed():
    root = Rule('root', ["untagged", "tagged<tag>"])
    grammar = Grammar({'root':root})

    succeed = "Failed to throw exception"
    try:
        output = grammar.generate('root<tag')
    except AttributeError as e:
        succeed = e.args[0]
    assert "Missing close '>' to tag in root rule: root<tag" == succeed

def test_grammar_tag_unopened():
    root = Rule('root', ["untagged", "tagged<tag>"])
    grammar = Grammar({'root':root})

    succeed = "Failed to throw exception"
    try:
        output = grammar.generate('root tag>')
    except AttributeError as e:
        succeed = e.args[0]
    assert "Unexpected close tag '>' (was no '<') in root rule: root tag>" == succeed

def test_operation():
    rule = Rule('root', ["[var:text]$var$"])
    grammar = Grammar({'root':rule})
    output = grammar.generate('root')
    assert "text" == output

def test_comma_rule():
    rule_rule = Rule('root', ['#a,b#'])
    rule_a = Rule('a', '1')
    rule_b = Rule('b', '2')
    rules = {}
    for rule in [rule_rule, rule_a, rule_b]:
        rules[rule.name] = rule
    grammar = Grammar(rules)
    output = grammar.generate()
    assert "12" == output

def test_comma_var():
    rule_var = Rule('root', ["[var1:text][var2: adventure]$var1,var2$"])
    grammar = Grammar({'root':rule_var})
    output = grammar.generate()
    assert "text adventure" == output

def test_comma_tag():
    root = Rule('root', ["#child<tag1><tag2>#"])
    child = Rule('child', ["wrong<tag1>", "wrong<tag2>", "wrong", "right<tag1><tag2>"])
    grammar = Grammar({'root':root,'child':child})
    for i in range(10):
        output = grammar.generate()
        assert "right" == output

def test_comma_operation():
    rule_var = Rule('root', ["[var1:text,var2: adventure]$var1,var2$"])
    grammar = Grammar({'root':rule_var})
    output = grammar.generate()
    assert "text adventure" == output

#TODO: THIS IS TITUS BODE
def titius_bode(a, b, n):
        return int(a + ((b - a) * 2 * (n-2)))

def test_galaxy():
    '''
    hot_zone = randint(1, 8)
    bio_zone = randint(hot_zone + 1, hot_zone + 15)
    cold_zone = randint(bio_zone + 1, bio_zone + 20)
    gas_zone = randint(cold_zone + 1, cold_zone + 50)
    frozen_zone = randint(gas_zone, gas_zone + 100)
    '''
    grammar = read_grammar("grammar/shitty_grammar.json")
    assert grammar
    gal_str = grammar.generate()
    assert gal_str
    assert len(gal_str) > 0
    print("gal_str " + gal_str)

    bit = gal_str.split(' ')
    # skip bit[0] because that is star
    hot_zone = randint(0, int(bit[1]))
    bio_zone = randint(hot_zone, hot_zone + int(bit[2]))
    cold_zone = randint(bio_zone, bio_zone + int(bit[3]))
    gas_zone = randint(cold_zone, cold_zone + int(bit[4]))
    frozen_zone = randint(gas_zone, gas_zone + int(bit[5]))

    print(" zones: " + str([hot_zone,bio_zone,cold_zone,gas_zone,frozen_zone]))
    '''
    "_dynamic_tag": ["[star_type:#star_type<$star$>#]"],

    num_planets = randint(2, 10)
    p1 = 6 + randint(3, 10)
    p2 = randint(p1+3, p1+7)
    current_angle = 0
    for i in range(1,num_planets):
        current_angle = current_angle + 120
        if i == 1:
            planet_radius = p1 * self.system_scalar
        elif i == 2:
            planet_radius = p2 * self.system_scalar
        else:
            planet_radius = self.titius_bode(p1, p2, i) * self.system_scalar
    '''
    num_planets = randint(2, 10)
    p1 = 8 + randint(1, 8)
    p2 = p1 + 2 + randint(1, 5)
    current_angle = 0
    planet_array = []
    for i in range(1, num_planets + 1):
        current_angle = current_angle + 120
        if i == 1:
            planet_radius = p1
        elif i == 2:
            planet_radius = p2
        else:
            planet_radius = titius_bode(p1, p2, i)
        if planet_radius < hot_zone:
            planet = grammar.generate('planet<hot>')
        elif planet_radius < bio_zone:
            planet = grammar.generate('planet<bio>')
        elif planet_radius < cold_zone:
            planet = grammar.generate('planet<cold>')
        elif planet_radius < gas_zone:
            planet = grammar.generate('planet<gas>')
        elif planet_radius < frozen_zone:
            planet = grammar.generate('planet<frozen>')
        else:
            planet = 'frozen_belt'
        planet_array.append({'radius': planet_radius, 'angle': current_angle, 'planet': planet})

    print(f"PLANET {planet_array}")
    assert False

def test_story():
    # grammar generation demo for non-programmers
    grammar = read_grammar("grammar/shitty_grammar.json")
    for i in range(10):
        print(grammar.generate("story"))
    # assert False
