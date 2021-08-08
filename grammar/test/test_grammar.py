from grammar.grammar import Grammar
from grammar.grammar import Rule

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
    rule = Rule('tagged', ["has<tag>"])
    assert rule
    exp = rule.select_child()
    assert "has" == exp
    exp = rule.select_child([])
    assert "has" == exp

def test_tag_invoke():
    rule = Rule('tagged', ["has<tag>", "doesn't have tag"])
    assert rule
    for i in range(10):
        exp = rule.select_child(['tag'])
        assert "has" == exp

def test_tag_multi_invoke():
    rule = Rule('tagged', ["has<tag><other>", "doesn't have other tag<tag>", "doesn't have tag tag<other>"])
    assert rule
    for i in range(10):
        exp = rule.select_child(['tag', 'other'])
        assert "has" == exp