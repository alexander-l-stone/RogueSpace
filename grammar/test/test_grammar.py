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
    # if we pass a tag, we should be allowed to get tagged results
    root = Rule('root', ["#tagged<tag>#"])
    rule = Rule('tagged', ["has<tag>"])
    grammar = Grammar({'root':root,'tagged':rule})

    output = grammar.generate()
    assert "has" == output

    # if we don't pass a tag, we should not be allowed to get tagged results
    root = Rule('root', ["#tagged#"])
    rule = Rule('tagged', ["has<tag>"])
    grammar = Grammar({'root':root,'tagged':rule})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_grammar_multi_tag():
    root = Rule('root', ["#<tag>tagged<other>#"]) # acceptable to invoke tag from anywhere
    rule = Rule('tagged', ["has<tag><other>", "doesn't have other tag<tag>", "doesn't have tag tag<other>"])
    grammar = Grammar({'root':root,'tagged':rule})
    for i in range(10):
        output = grammar.generate()
        assert "has" == output

def test_grammar_tag_root():
    root = Rule('root', ["tagged<tag>"])
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
    root = Rule('root', ["#child<tag1,tag2>#"])
    child = Rule('child', ["right<tag1><tag2>"])
    grammar = Grammar({'root':root,'child':child})
    output = grammar.generate()
    assert "right" == output

    root = Rule('root', ["#child<tag1,tag2>#"])
    child = Rule('child', ["wrong<tag1>"])
    grammar = Grammar({'root':root,'child':child})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("No valid expansions for tags")

def test_comma_operation():
    rule_var = Rule('root', ["[var1:text,var2: adventure]$var1,var2$"])
    grammar = Grammar({'root':rule_var})
    output = grammar.generate()
    assert "text adventure" == output

def test_function():
    root = Rule('root', ["[var:ant.capitalize]$var$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "Ant" == output

def test_function_args():
    root = Rule('root', ["[var:ant.capitalize()]$var$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "Ant" == output

    root = Rule('root', ["[var:pants.remove(ant)]$var$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "ps" == output

def test_function_multi():
    root = Rule('root', ["[var:pants.remove(p).capitalize]$var$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "Ants" == output
    
    root = Rule('root', ["[var:pants.capitalize.remove(P)]$var$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "ants" == output

def test_function_rule():
    root = Rule('root', ["#child.capitalize#"])
    child = Rule('child', ["ant"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "Ant" == output

def test_function_rule_args():
    root = Rule('root', ["#child.remove(ant)#"])
    child = Rule('child', ["pants"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "ps" == output

def test_function_rule_multi():
    root = Rule('root', ["#child.remove(p).capitalize#"])
    child = Rule('child', ["pants"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "Ants" == output
    
    root = Rule('root', ["#child.capitalize.remove(P)#"])
    child = Rule('child', ["pants"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "ants" == output

def test_function_var():
    root = Rule('root', ["[var:ant]$var.capitalize$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "Ant" == output

def test_function_rule_var():
    root = Rule('root', ["[var:pants]$var.remove(ant)$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "ps" == output

def test_function_var_multi():
    root = Rule('root', ["[var:pants]$var.remove(p).capitalize$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "Ants" == output
    
    root = Rule('root', ["[var:pants]$var.capitalize.remove(P)$"])
    grammar = Grammar({'root':root})
    output = grammar.generate()
    assert "ants" == output

def test_function_tag():
    root = Rule('root', ["#child<ant.capitalize>#"])
    child = Rule('child', ["text<Ant>"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "text" == output

def test_function_tag_args():
    root = Rule('root', ["#child<pants.remove(ant)>#"])
    child = Rule('child', ["text<ps>"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "text" == output

def test_function_tag_multi():
    root = Rule('root', ["#child<pants.remove(p).capitalize>#"])
    child = Rule('child', ["text<Ants>"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "text" == output
    
    root = Rule('root', ["#child<pants.capitalize.remove(P)>#"])
    child = Rule('child', ["text<ants>"])
    grammar = Grammar({'root':root, 'child':child})
    output = grammar.generate()
    assert "text" == output

def test_function_args_missing_close():
    root = Rule('root', ["[a.capitalize() ]"])
    grammar = Grammar({'root':root})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("Function call not at end of invocation.")

    root = Rule('root', ["#child.capitalize() #"])  
    child = Rule('child', ["a"])
    grammar = Grammar({'root':root,'child':child})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("Function call not at end of invocation.")

    root = Rule('root', ["[var:a]$var.capitalize() $"])
    grammar = Grammar({'root':root})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("Function call not at end of invocation.")

    root = Rule('root', ["#child<tag.capitalize() >#"])  
    child = Rule('child', ["a"])
    grammar = Grammar({'root':root,'child':child})

    output = "Failed to throw exception"
    try:
        output = grammar.generate()
    except AttributeError as e:
        output = e.args[0]
    assert output.startswith("Function call not at end of invocation.")

def test_story():
    # grammar generation demo for non-programmers
    grammar = read_grammar("grammar/shitty_grammar.json")
    for i in range(10):
        print(grammar.generate("story"))
    # assert False
