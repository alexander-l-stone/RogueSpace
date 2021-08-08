import math
import json
from random import seed, randint

'''
    Grammar = file
        rule named "root" is reserved as the start point

        variables dict 
        user-cached data: user can create and reference variable

    global function library
    "#noun.cap#"

    Rule
    name = [expansion1, expansion2, ...]

    tagging system?

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
'''
#TODO: Allow different tags to add a different weight to the same rule
# TODO consider a way to functionalize scope parses for reusability (don't break trampoline rule)

class Grammar:
    def __init__(self, rules:dict):
        self.rules = rules # name to obj

    # TODO make a grammar visualizer
    # TODO preparse rules into a node tree to optimize generation

    # TODO turn debug prints into logging so they can be toggled

    def generate(self, root='root'):
        # TODO parse tags
        if root not in self.rules:
            raise AttributeError(f"No rule named \"{root}\" to start from")
        return self.expand_rule(self.rules[root])

    def expand_rule(self, rule):
        exp:str = rule.select_child()
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
                    raise AttributeError(f"rule name not found: {rule_name}\ncurrent output: {output}\nstack:{parent_stack}")
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

            # print(f"\nFRAME UNPACK: ")
        
        # print(f"START FRAME\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\ni={i} EXP {exp}\nSCOPE {scope}\nOUTPUT {output}\n")
        

        # TODO implement
        # weight should be preparsed
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
            elif scope[-1]['scope_type'] == '#':
                # check if scope starts with a varstore
                # parse scope body as a rule name to expand
                # check for final func execution
                if char == ':':
                    # previous is a var store
                    scope[-1]['varstore'] = scope[-1]['token']
                    scope[-1]['token'] = ''
                elif char == '.':
                    scope.append({'scope_type':'.'})
                    scope[-1]['token'] = ''
                    exp_frame = self.__make_exp_frame(exp, scope, output, i+1)
                    parent_stack.append(exp_frame)
                    # print(f"\nFRAME ADD\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\nRULE CALL {scope[-2]['token']}\n")
                    return (user_vars, parent_stack, output, scope[-2]['token'])
                elif char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '<':
                    scope.append({'scope_type':'<', 'token':''})
                elif char == '#':
                    exp_frame = self.__make_exp_frame(exp, scope, output, i+1)
                    parent_stack.append(exp_frame)
                    # print(f"\nFRAME ADD\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\nRULE CALL {scope[-1]['token']}\n")
                    return (user_vars, parent_stack, output, scope[-1]['token'])
                else:
                    scope[-1]['token'] += char
                # print(f"token {scope[-1]['token']}")
            elif scope[-1]['scope_type'] == '$':
                if char == '$':
                    # output var to outer scope (which may be literal output), clear state
                    var_name = scope[-1]['token']
                    if var_name not in user_vars:
                        raise AttributeError(f"var not defined before use: {scope[-1]['token']}\ncurrent output: {output}\nstack:{parent_stack}")
                    scope.pop()
                    if len(scope) == 0:
                        output += user_vars[var_name]
                    else:
                        scope[-1]['token'] += user_vars[var_name]
                else:
                    scope[-1]['token'] += char
            elif scope[-1]['scope_type'] == '<':
                if char == '$':
                    scope.append({'scope_type':'$', 'token':''})
                elif char == '>':
                    # output var to outer scope (which may be literal output), clear state
                    tag = scope[-1]['token']
                    popped_scope = scope.pop()
                    if len(scope) == 0:
                        # impossible
                        raise AttributeError(f"impossible tag lookup in outside scope: tag: {tag}\nscope: {popped_scope}\ncurrent output: {output}\nstack:{parent_stack}")
                    elif scope[-1]['scope_type'] == "#":
                        if 'tags' not in scope[-1]:
                            scope[-1]['tags'] = [tag]
                        else:
                            scope[-1]['tags'].append(tag)
                else:
                    scope[-1]['token'] += char
            elif scope[-1]['scope_type'] == '[':
                # TODO
                pass
            elif scope[-1]['scope_type'] == '.':
                # TODO
                pass
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

class Rule:
    def __init__(self, name:str, expansions:list):
        self.name = name
        self.expansions = {} # str expansion -> tuple(int weight, array[str] tags)
        #TODO precalculate tag mapping
        for exp in expansions:
            # if the string starts with a number and a %, strip that off as a weight
            numstr = ''
            inserted = False
            for char in exp:
                if char == '\\':
                    continue
                if not char.isdigit() and char != '%':
                    self.expansions[exp] = (1, [])
                    inserted = True
                    break
                if char != '%':
                    numstr += char
                elif numstr == '':
                    raise AttributeError(f"Null weight. Rule: {name} Expansion: {exp}")
                else:
                    self.expansions[exp[len(numstr)+1:]] = (int(numstr), [])
                    inserted = True
                    break
            if not inserted:
                self.expansions[exp] = (1, [])
        # strip tags and escapes
        changed_dict = {}
        for exp,data in self.expansions.items():
            tag_ind = None
            i = 0
            while i < len(exp):
                if i >= len(exp):
                    break
                char = exp[i]
                if char == '\\':
                    i += 1 # skip the character after the \
                elif char == '<':
                    tag_ind = i
                elif tag_ind is not None:
                    if char in "#$<[]":
                        raise AttributeError(f"Illegal use of 'special character '{char}' inside tag. Rule: {name} Expansion: {exp}")
                    if char == '>':
                        data[1].append(exp[tag_ind+1:i]) # TODO inclusive end index?
                        exp = exp[0:tag_ind] + exp[i+1:]
                        i = tag_ind - 1 # the loop will increment
                        tag_ind = None
                else:
                    break
                i += 1
            # add self to the new dict so we don't need to modify the old one during iteration
            changed_dict[exp] = data
        self.expansions = changed_dict

    # TODO add argument to filter by tag
    def select_child(self, tags=None)->str:
        '''
        Randomly select an expansion by weight
        If a tag is provided, only consider expansions which have that tag
        '''
        total_weight = 0
        for exp,data in self.expansions.items():
            if tags is not None:
                should_continue = False
                for tag in tags:
                    if tag not in data[1]:
                        print(f'{tag} not in {data[1]}')
                        should_continue = True
                        continue
                    print(f'{tag} yes in {data[1]}')
                if should_continue:
                    continue

            total_weight += data[0]

        if total_weight == 0:
            raise AttributeError(f"No valid expansions for tags {tags} in rule {self}")

        rand = randint(1, total_weight)
        for exp,data in self.expansions.items():
            if tags is not None:
                should_continue = False
                for tag in tags:
                    if tag not in data[1]:
                        should_continue = True
                        continue
                if should_continue:
                    continue

            rand -= data[0]
            if rand <= 0:
                return exp
        # unreachable
        return None
    
    def __repr__(self):
        return '"' + self.name + '" : ' + str(self.expansions)

    def __str__(self):
        return '"' + self.name + '" : ' + str(self.expansions)

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