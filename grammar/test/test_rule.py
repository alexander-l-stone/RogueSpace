
from grammar.rule import Rule

def test_rule():
    name = "rule_name"
    expansions = ["exp1", f"23%exp2"]
    rule = Rule(name, expansions)
    assert rule
    assert rule.name == name
    assert {"exp1":(1,{},"exp1"),"exp2":(23,{},"exp2")} == rule.expansions

def test_rule_missing_weight():
    name = "rule_name"
    expansions = ["exp1", f"%exp2"]

    err = "Failed to throw exception"
    try:
        rule = Rule(name, expansions)
    except AttributeError as e:
        err = e.args[0]
    assert f"Null weight. Rule: rule_name Expansion: %exp2" == err

def test_select_child():
    rule = Rule('root', ["succeed"])
    assert "succeed" == rule.select_child()
    assert "succeed" == rule.select_child([])

def test_tag():
    rule = Rule('tagged', ["has<tag>"])
    assert rule
    assert {"has<tag>":(1,{"tag":None},"has")} == rule.expansions

    output = "Failed to throw exception"
    try:
        output = rule.select_child()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_tag_invoke():
    rule = Rule('tagged', ["has<tag>"])
    assert rule
    assert {"has<tag>":(1,{"tag":None},"has")} == rule.expansions

    # will error if bad, which fails test
    output = rule.select_child(["tag"])
    assert "has" == output

    rule = Rule('tagged', ["<tag>"])
    assert rule
    assert {"<tag>":(1,{"tag":None},"")} == rule.expansions
    output = rule.select_child(["tag"])
    assert "" == output

def test_tag_negate():
    rule = Rule('root', ["fail<^tag>"])
    assert rule
    assert {"fail<^tag>":(1,{"^tag":None},"fail")} == rule.expansions

    output = "Failed to throw exception"
    try:
        output = rule.select_child(["tag"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_tag_invoke_negative():
    rule = Rule('root', ["fail<tag>"])
    assert {"fail<tag>":(1,{"tag":None},"fail")} == rule.expansions
    
    output = "Failed to throw exception"
    try:
        output = rule.select_child(["^tag"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_tag_invoke_block():
    rule = Rule('root', ["text<tag&other>"])
    assert { "text<tag&other>" : (1,{"tag&other":None},"text") } == rule.expansions

    output = "Failed to throw exception"
    try:
        output = rule.select_child(["tag"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

    output = "Failed to throw exception"
    try:
        output = rule.select_child(["other"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

    output = rule.select_child(["other", "tag"])
    assert "text" == output

def test_tag_multi_declare():
    rule = Rule('tagged', ["has<tag><other>"])
    assert rule
    assert { "has<tag><other>" : (1,{"tag":None,"other":None},"has") } == rule.expansions

    output = rule.select_child(['tag'])
    assert "has" == output

    output = rule.select_child(['other'])
    assert "has" == output

def test_tag_comma_declare():
    rule = Rule('tagged', ["has<tag,other>"])
    assert rule
    assert { "has<tag,other>" : (1,{"tag":None,"other":None},"has") } == rule.expansions

    output = rule.select_child(['tag'])
    assert "has" == output

    output = rule.select_child(['other'])
    assert "has" == output

def test_tag_multi_invoke():
    rule = Rule('tagged', ["has<tag>", "has<other>"])
    assert rule
    assert {
            "has<tag>" : (1,{"tag":None},"has"),
            "has<other>" : (1,{"other":None},"has")
           } == rule.expansions

    output = "Failed to throw exception"
    try:
        output = rule.select_child(["tag","other"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_tag_weighted():
    rule = Rule('tagged', [f"0%text<2%tag>"])
    assert rule
    assert { "text<tag>" : (0,{"tag":2},"text") } == rule.expansions

    # without tag, use default weight 0 (invalid)
    output = "Failed to throw exception"
    try:
        output = rule.select_child()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

    # with tag, use tag weight 2
    output = rule.select_child(["tag"])
    assert "text" == output

def test_duplicate_expansion():
    rule = Rule("dup", [f'2%a<7%tag>', f'3%a<11%tag><17%other>', f'a<19%other>'])
    assert {
        'a<tag>' : (2, { 'tag' : 7 }, 'a'),
        'a<tag><other>' : (3, { 'tag' : 11, 'other' : 17 }, 'a'),
        'a<other>' : (1, { 'other' : 19 }, 'a'),
    } == rule.expansions

    rule = Rule("dup", [f'2%a<7%tag>', f'3%a<11%tag>'])
    assert { 'a<tag>' : (5, { 'tag' : 18 }, 'a') } == rule.expansions

def test_tag_unopened():
    output = "Failed to throw exception"
    try:
        rule = Rule('tagged', ["unopened tag>"])
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("Unopened tag in rule")