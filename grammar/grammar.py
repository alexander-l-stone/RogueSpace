import math
import json

from grammar.rule import Rule

'''
    Grammar = file
        rule named "root" is reserved as the start point

        variables dict 
        user-cached data: user can create and reference variable

    global function library
    "#noun.cap#"

    Rule
    name = [expansion1, expansion2, ...]

    syntax so far
    #rule#
    [runWithoutOutput]
    [var:val] store value in variable
    [var:#ruleOutputAsVal#] store rule output in variable named var
    #var:rule# store rule output in variable named var, and output
    $unpackVar$ output variable to text
    <tag> metadata in a result
    #invoke<tag,tag2># require tag(s) in generation result
    [unpackVar] output a var to text
    \\ escape char
    #rule.func(arg)# apply a function to a rule (with arguments)
    #$varOfRule$# not technically a syntax - replaces var with value and evaluates as a rule name
    #prefix$postfix$# complexity!
    2% weight the following at 2 (default weight is 1)

    reserved chars
    \\[]:#$%<>

    weights must be initial
    tags for an expansion must be final
'''
#TODO: Allow different tags to add a different weight to the same rule
# TODO consider a way to functionalize scope parses for reusability (don't break trampoline rule)

class Grammar:
    def __init__(self, rules:dict):
        self.rules = rules # name to obj

    # TODO make a grammar visualizer
    # TODO preparse rules into a node tree to optimize generation

    # TODO handle unclosed scope errors

    # TODO turn debug prints into logging so they can be toggled

    def generate(self, root='root'):
        # parse tags
        i = 0
        token_start = None
        tags = []
        while i < len(root):
            char = root[i]
            if char in'#$[]':
                raise AttributeError(f"Bad rule name (illegal char '{char}') for root rule: {root}")
            elif char == '<':
                if token_start is None:
                    token_start = i
                else:
                    raise AttributeError(f"Bad tag (extra '<') in root rule: {root}")
            elif char == '>' or char == ',':
                if token_start is None:
                    raise AttributeError(f"Unexpected close tag '>' (was no '<') in root rule: {root}")
                # add to the tags list
                tags.append(root[token_start+1:i])
                # remove tag from the rule lookup name
                root = root[0:token_start] + root[i+1:]
                i -= i - token_start
                # if chained tag, start counting the new tag
                if char == ',':
                    token_start = i
                else:
                    token_start = None
            i += 1
        if token_start is not None:
            raise AttributeError(f"Missing close '>' to tag in root rule: {root}")

        # fetch rule and generate
        if root not in self.rules:
            raise AttributeError(f"No rule named \"{root}\" to start from")
        return self.expand_rule(self.rules[root], tags)

    def expand_rule(self, rule, tags):
        exp:str = rule.select_child(tags)
        ret = self.__expand_rule_helper({}, [], '', True, exp)
        while True:
            # print(f"EXPAND {ret}")
            if len(ret) == 4:
                # user_vars, parent_stack, output, rule_name
                user_vars = ret[0]
                parent_stack = ret[1]
                output = ret[2]
                rule_name = ret[3]
                if ret[3] in self.rules:
                    curr_rule = self.rules[rule_name]
                else:
                    raise AttributeError(f"rule name not found: {rule_name}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                if 'tags' in parent_stack[-1]['scope'][-1]:
                    child_expansion = curr_rule.select_child(parent_stack[-1]['scope'][-1]['tags'])
                else:
                    child_expansion = curr_rule.select_child()
                # print(f"\nrule_name {rule_name} rule {curr_rule} chosen exp {child_expansion}\n")
                ret = self.__expand_rule_helper(user_vars, parent_stack, output, True, child_expansion)
            elif len(ret) == 3:
                user_vars = ret[0]
                parent_stack = ret[1]
                output = ret[2]
                if len(parent_stack) > 0:
                    ret = self.__expand_rule_helper(user_vars, parent_stack, output, False, '')
                else:
                    break
        if len(ret[1]) != 0:
            user_vars = ret[0]
            parent_stack = ret[1]
            output = ret[2]
            raise AttributeError(f"Missing close '{parent_stack[-1]['scope_type']}'\ntoken: {parent_stack[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
        return ret[2]

    def __expand_rule_helper(self, user_vars:dict, parent_stack:list, child_output:str, newFrame:bool, exp:str):
        if newFrame:
            scope:list = []
            output = ''
            i = 0
        else:
            exp_frame = parent_stack.pop()

            exp = exp_frame['exp']
            scope:list = exp_frame['scope']
            output = exp_frame['output']
            i = exp_frame['i']
            
            # process output from previous rec level
            if scope[-1]['scope_type'] == '#':
                last_scope = scope.pop()
                if len(scope) == 0:
                    output += child_output
                else:
                    scope[-1]['token'] += child_output
                if 'varstore' in last_scope:
                    user_vars[last_scope['varstore']] = child_output
                if 'comma_rule' in last_scope:
                    scope.append({'scope_type':'#', 'token':''})

            # print(f"\nFRAME UNPACK: ")
        
        # print(f"START FRAME\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\ni={i} EXP {exp}\nSCOPE {scope}\nOUTPUT {output}\n")
        
        # pick an expansion at random
        # parse out the rule invocations, variable assignments, function invocations, etc
        # execute and recurse as necessary
        while i < len(exp):
            # in #
            # with .func()
            # in $
            # in []
            # in <>
            char = exp[i]
            # print(f"i {i} char {char}")

            if len(scope) == 0:
                # top level no scope
                # check for a scope begin char, else character is plaintext to output
                # no top level <> scope! preprocess tags
                if char == '#':
                    scope.append({'scope_type':'#', 'token':''})
                elif char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '[':
                    scope.append({'scope_type':'[', 'token':''})
                else:
                    output += char
            # below: handle each scope context

            # RULE INVOCATION
            elif scope[-1]['scope_type'] == '#':
                # check if scope starts with a varstore
                # parse scope body as a rule name to expand
                # check for final func execution
                if char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '<':
                    scope.append({'scope_type':'<', 'token':''})
                elif char == '[':
                    scope.append({'scope_type':'[', 'token':''})
                elif char == ':':
                    # previous is a var store
                    scope[-1]['varstore'] = scope[-1]['token']
                    scope[-1]['token'] = ''
                elif char == '.':
                    scope.append({'scope_type':'.'})
                    scope[-1]['token'] = ''
                    # recurse
                    exp_frame = self.__make_exp_frame(exp, scope, output, i+1)
                    parent_stack.append(exp_frame)
                    # print(f"\nFRAME ADD\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\nRULE CALL {scope[-2]['token']}\n")
                    return (user_vars, parent_stack, output, scope[-2]['token'])
                elif char == '#' or char == ',':
                    if char == ',':
                        scope[-1]['comma_rule'] = True
                    exp_frame = self.__make_exp_frame(exp, scope, output, i+1)
                    # recurse
                    parent_stack.append(exp_frame)
                    # print(f"\nFRAME ADD\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\nRULE CALL {scope[-1]['token']}\n")
                    return (user_vars, parent_stack, output, scope[-1]['token'])
                else:
                    scope[-1]['token'] += char
                # print(f"token {scope[-1]['token']}")

            # VARIABLE DEREFERENCE
            elif scope[-1]['scope_type'] == '$':
                if char == '#':
                    scope.append({'scope_type':'#', 'token':''})
                elif char == '<':
                    raise AttributeError(f"Illegal tag invocation in variable dereference ('<' in '$$' block): {scope[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                elif char == '[':
                    scope.append({'scope_type':'[', 'token':''})
                if char == '$' or char == ',':
                    # output var to outer scope (which may be literal output), clear state
                    var_name = scope[-1]['token']
                    if var_name not in user_vars:
                        raise AttributeError(f"var not defined before use: {scope[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                    scope.pop()
                    if len(scope) == 0:
                        output += user_vars[var_name]
                    else:
                        scope[-1]['token'] += user_vars[var_name]
                    if char == ',':
                        scope.append({'scope_type':'$', 'token':''})
                else:
                    scope[-1]['token'] += char

            # TAG INVOCATION
            elif scope[-1]['scope_type'] == '<':
                if char == '#':
                    scope.append({'scope_type':'#', 'token':''})
                elif char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '[':
                    scope.append({'scope_type':'[', 'token':''})
                elif char == '>' or char == ',':
                    # output var to outer scope (which may be literal output), clear state
                    tag = scope[-1]['token']
                    popped_scope = scope.pop()
                    if len(scope) == 0:
                        # impossible
                        raise AttributeError(f"impossible tag lookup in outside scope ('<>' block survived parse strip): tag: {tag}\nscope: {popped_scope}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                    elif scope[-1]['scope_type'] == "#":
                        if 'tags' not in scope[-1]:
                            scope[-1]['tags'] = [tag]
                        else:
                            scope[-1]['tags'].append(tag)
                    if char == ',':
                        scope.append({'scope_type':'<', 'token':''})
                else:
                    scope[-1]['token'] += char

            # OPERATION EXECUTION
            elif scope[-1]['scope_type'] == '[':
                if char == '#':
                    scope.append({'scope_type':'#', 'token':''})
                if char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '<':
                    raise AttributeError(f"Illegal tag invocation in operation execution ('<' in '[]' block): {scope[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                elif char == '[':
                    raise AttributeError(f"Illegal nested operation (open '[' in '[]' block): {scope[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                elif char == '.':
                    raise AttributeError(f"Illegal function execution ('.' in '[]' block) in operation: {scope[-1]['token']}\ncurrent output: {output}\nuser_vars {user_vars}\nstack:{parent_stack}")
                elif char == ':':
                    # previous is a var store
                    scope[-1]['varstore'] = scope[-1]['token']
                    scope[-1]['token'] = ''
                elif char == ']' or char == ',':
                    exec_ret = scope[-1]['token']
                    popped_scope = scope.pop()
                    if 'varstore' in popped_scope:
                        user_vars[popped_scope['varstore']] = exec_ret
                    if char == ',':
                        scope.append({'scope_type':'[', 'token':''})
                else:
                    scope[-1]['token'] += char

            # FUNCTION INVOCATION
            elif scope[-1]['scope_type'] == '.':
                # TODO
                # TODO check for enclosing scope close as alternate to '('
                pass

            # FUNCTION ARGUMENTS
            elif scope[-1]['scope_type'] == '.(':
                # TODO
                pass

            i += 1
        
        # output to higher level
        # print(f"FRAME EXIT\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\n")
        return (user_vars, parent_stack, output)

    def __make_exp_frame(self, exp, scope, output, i):
        frame = {}
        frame['exp'] = exp
        frame['scope'] = scope
        frame['output'] = output
        frame['i'] = i
        return frame

    def parse_dollar(self, text, index):
        '''
        parse the inside of a variable unpacking
        index is the index of the open dollar
        '''
        # TODO implemetn
        pass

def read_grammar(fileName:str):
    '''
    throws FileNotFoundException
    '''
    with open(fileName, 'rb') as grammar_file:
        grammar_dict = json.load(grammar_file)

    rules = {}
    for name,expansions in grammar_dict.items():
        rules[name] = Rule(name, expansions)
    return Grammar(rules)