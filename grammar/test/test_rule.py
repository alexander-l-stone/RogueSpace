
from grammar.rule import Rule

def test_rule():
    name = "rule_name"
    expansions = ["exp1", f"23%exp2"]
    rule = Rule(name, expansions)
    assert rule
    assert rule.name == name
    assert {"exp1":(1,{}),"exp2":(23,{})} == rule.expansions

def test_rule_missing_weight():
    name = "rule_name"
    expansions = ["exp1", f"%exp2"]

    err = "Failed to throw exception"
    try:
        rule = Rule(name, expansions)
    except AttributeError as e:
        err = e.args[0]
    assert f"Null weight. Rule: rule_name Expansion: %exp2" == err

def test_tag():
    rule = Rule('tagged', ["has<tag>"])
    assert rule
    assert {"has":(1,{"tag":None})} == rule.expansions
    exp = rule.select_child()
    assert "has" == exp
    exp = rule.select_child([])
    assert "has" == exp
    
def test_tag_invoke():
    rule = Rule('tagged', ["has<tag>", "doesn't have tag"])
    assert rule
    assert {"has":(1,{"tag":None}),"doesn't have tag":(1,{})} == rule.expansions
    for i in range(10):
        exp = rule.select_child(['tag'])
        assert "has" == exp

def test_tag_multi_invoke():
    rule = Rule('tagged', ["has<tag><other>", "doesn't have 'other' tag<tag>", "doesn't have 'tag' tag<other>"])
    assert rule
    assert {"has" : (1,{"tag":None,"other":None}),
            "doesn't have 'other' tag" : (1,{"tag":None}),
            "doesn't have 'tag' tag" : (1,{"other":None})
           } == rule.expansions
    for i in range(10):
        exp = rule.select_child(['tag', 'other'])
        assert "has" == exp

def test_tag_weighted():
    rule = Rule('tagged', [f"0%weighted<2%tag>", f"unweighted<0%tag>"])
    assert rule
    for i in range(10):
        exp = rule.select_child()
        assert "unweighted" == exp
    for i in range(10):
        exp = rule.select_child(['tag'])
        assert "weighted" == exp