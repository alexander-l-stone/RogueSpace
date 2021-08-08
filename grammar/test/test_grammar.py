from grammar.grammar import Grammar
from grammar.grammar import Rule
from grammar.grammar import read_grammar
from random import randint

def test_rule():
    name = "rule_name"
    expansions = ["exp1", f"23%exp2"]
    rule = Rule(name, expansions)
    assert rule
    assert rule.name == name
    assert rule.expansions == {"exp1":(1,[]),"exp2":(23,[])}

def test_rule_missing_weight():
    name = "rule_name"
    expansions = ["exp1", f"%exp2"]

    # TODO make sure we have the correct error
    succeed = "Failed to throw exception"
    try:
        rule = Rule(name, expansions)
    except(AttributeError):
        succeed = True
    assert succeed is True

def test_grammar():
    rules = { 'root':Rule('root',["This story is #adj#"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    assert grammar
    assert grammar.rules == rules

def test_missing_root():
    rules = {}
    grammar = Grammar(rules)

    # TODO make sure we have the correct error
    succeed = "Failed to throw exception"
    try:
        grammar.generate()
    except(AttributeError):
        succeed = True
    assert succeed is True

def test_expansion():
    rules = { 'root':Rule('root',["This story is #adj# #adj#"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert output == "This story is the best the best"

def test_missing_variable():
    rules = { 'root':Rule('root',["This story is #adj# $var$"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)

    # TODO make sure we have the correct error
    succeed = "Failed to throw exception"
    try:
        grammar.generate()
    except(AttributeError):
        succeed = True
    assert succeed is True

def test_variable():
    rules = { 'root':Rule('root',["This story is #var:adj# $var$"]), 'adj':Rule('adj',["the best"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert output == "This story is the best the best"

def test_dynamic_rule():
    rules = { 'root':Rule('root',["This story is #var:adj# #$var$#"]), 'adj':Rule('adj',["the best"]), 'the best':Rule("the best",["and dynamic"]) }
    grammar = Grammar(rules)
    output = grammar.generate()
    assert output
    assert output == "This story is the best and dynamic"

def test_tag():
    rule = Rule('tagged', ["<tag>has"])
    assert rule
    exp = rule.select_child()
    assert "has" == exp
    exp = rule.select_child([])
    assert "has" == exp

def test_tag_invoke():
    rule = Rule('tagged', ["<tag>has", "doesn't have tag"])
    assert rule
    for i in range(10):
        exp = rule.select_child(['tag'])
        assert "has" == exp

def test_tag_multi_invoke():
    rule = Rule('tagged', ["<tag><other>has", "<tag>doesn't have other tag", "<other>doesn't have tag tag"])
    assert rule
    for i in range(10):
        exp = rule.select_child(['tag', 'other'])
        assert "has" == exp

def test_grammar_tag():
    root = Rule('root', ["#tagged<tag>#"])
    rule = Rule('tagged', ["<tag>has", "doesn't have tag"])
    grammar = Grammar({'root':root,'tagged':rule})
    for i in range(10):
        output = grammar.generate()
        assert "has" == output

def test_grammar_multi_tag():
    root = Rule('root', ["#<tag>tagged<other>#"])
    rule = Rule('tagged', ["<tag><other>has", "<tag>doesn't have other tag", "<other>doesn't have tag tag"])
    grammar = Grammar({'root':root,'tagged':rule})
    for i in range(10):
        output = grammar.generate()
        assert "has" == output

def titus_bode(a, b, n):
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
    hot_zone = randint(1, int(bit[1]))
    bio_zone = randint(hot_zone + 1, hot_zone + int(bit[2]))
    cold_zone = randint(bio_zone + 1, bio_zone + int(bit[3]))
    gas_zone = randint(cold_zone + 1, cold_zone + int(bit[4]))
    frozen_zone = randint(gas_zone + 1, gas_zone + int(bit[5]))

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
            planet_radius = self.titus_bode(p1, p2, i) * self.system_scalar
    '''
    planet_radius = randint(1,frozen_zone)
    if planet_radius < hot_zone:
        planet = grammar.generate('planet_hot')
    elif planet_radius < bio_zone:
        planet = grammar.generate('planet_bio')
    elif planet_radius < cold_zone:
        planet = grammar.generate('planet_cold')
    elif planet_radius < gas_zone:
        planet = grammar.generate('planet_gas')
    elif planet_radius < frozen_zone:
        planet = grammar.generate('planet_frozen')
    else:
        pass

    print(f"PLANET {planet}")
    assert False
