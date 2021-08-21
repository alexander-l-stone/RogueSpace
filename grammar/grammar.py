import math
import json

from grammar.rule import Rule
from grammar.function_library_parser import parse_library_file
import grammar.universal_function_library as universal_function_library

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

    Special syntax:
    <tag&tag2> tag AND tag2

    reserved chars
    \\[]:#$%<>

    weights must be initial
    tags for an expansion must be final
'''
#TODO: Allow different tags to add a different weight to the same rule
# TODO consider a way to functionalize scope parses for reusability (don't break trampoline rule)

class Grammar:
    def __init__(self, rules:dict, function_library:dict=None):
        self.rules = rules # name to obj
        if function_library is None:
            function_library = {}
        self.func_lib = parse_library_file(universal_function_library)
        self.func_lib |= function_library

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

    def expand_rule(self, rule:object, tags:list):
        
        user_vars = {}
        frame_stack = []
        exp:str = rule.select_child(tags)
        
        scope:list = None # it will get clobbered soon, it just needs to exist outside loop scope
        natural_exp_end = False
        first = True
        if not frame_stack or first:
            first = False
            # print(f"START FRAME\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\ni={i} EXP {exp}\nSCOPE {scope}\nOUTPUT {output}\n")
            if natural_exp_end:
                exp_frame = frame_stack.pop()

                child_output = scope[0]['token']

                exp = exp_frame['exp']
                scope = exp_frame['scope']
                i = exp_frame['i']
                
                # process output from previous rec level
                if scope[-1]['scope_type'] == '#':
                    last_scope = scope.pop()
                    # instead transition to function parse if it was 'closed' with a dot
                    if 'dot_rule' in last_scope:
                        scope.append({'scope_type':'.', 'token':'', 'close_char':'#', 'args':[child_output]})
                        if 'varstore' in last_scope:
                            scope[-1]['varstore'] = last_scope['varstore']
                    else:
                        # output
                        scope[-1]['token'] += child_output
                        if 'varstore' in last_scope:
                            user_vars[last_scope['varstore']] = child_output
                        # chain the # parse if it was 'closed' with a comma
                        if 'comma_rule' in last_scope:
                            scope.append({'scope_type':'#', 'token':''})
                # print(f"\nFRAME UNPACK: ")
            else:
                scope:list = [{'scope_type':'output', 'token':''}]
                i = 0
            natural_exp_end = True

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
                if char == '\\':
                    # if escaped, output next char directly
                    scope[-1]['token'] += exp[i+1]
                    i += 2
                    continue

                # print(f"i {i} char {char}")

                if scope[-1]['scope_type'] == 'output':
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
                        scope[-1]['token'] += char
                elif len(scope) == 1:
                    self.raise_parse_error(f"Root scopt is not output", scope, user_vars, frame_stack)
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
                    elif char in '#,.':
                        # if close was a comma, chain
                        # because the execution is done in the main function b/c trampoline, pass it as a flag
                        if char == ',':
                            scope[-1]['comma_rule'] = True
                        # if close was a dot, invoke function
                        if char == '.':
                            scope[-1]['dot_rule'] = True
                        exp_frame = self.__make_exp_frame(exp, scope, i+1)
                        # recurse
                        frame_stack.append(exp_frame)
                        # print(f"\nFRAME ADD\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\nRULE CALL {scope[-1]['token']}\n")
                        # TODO lookup rule name, overwrite current frame
                        rule_name = scope[-1]['token']
                        tags = scope[-1]['tags'] if 'tags' in scope[-1] else []
                        if rule_name in self.rules:
                            exp = self.rules[rule_name].select_child(tags)
                        else:
                            self.raise_parse_error(f"rule name not found: {rule_name}", scope, user_vars, frame_stack)
                        natural_exp_end = False
                        break
                    else:
                        scope[-1]['token'] += char
                    # print(f"token {scope[-1]['token']}")

                # VARIABLE DEREFERENCE
                elif scope[-1]['scope_type'] == '$':
                    if char == '#':
                        scope.append({'scope_type':'#', 'token':''})
                    elif char == '<':
                        raise AttributeError(f"Illegal tag invocation in variable dereference ('<' in '$$' block): {scope[-1]['token']}", user_vars, frame_stack)
                    elif char == '[':
                        scope.append({'scope_type':'[', 'token':''})
                    if char in '$.,':
                        # output var to outer scope (which may be literal output), clear state
                        popped_scope = scope.pop()
                        var_name = popped_scope['token']
                        if var_name not in user_vars:
                            self.raise_parse_error(f"var not defined before use: {popped_scope['token']}", scope, user_vars, frame_stack)
                        deref_val = user_vars[var_name]
                        # if close was a dot, invoke function before output
                        if char == '.':
                            scope.append({'scope_type':'.', 'token':'', 'close_char':'$', 'args':[deref_val]})
                            if 'varstore' in popped_scope:
                                scope[-1]['varstore'] = popped_scope['varstore']
                        else:
                            # output
                            scope[-1]['token'] += deref_val
                            # if close was a comma, chain
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
                    elif char == ':':
                        self.raise_parse_error(f"Illegal variable store in tag invocation (':' in '<>' block): {scope[-1]['token']}", scope, user_vars, frame_stack)
                    elif char in '>,.':
                        # output var to outer scope (which may be literal output), clear state
                        tag = scope[-1]['token']
                        if len(scope) < 3:
                            # impossible
                            self.raise_parse_error(f"impossible tag lookup in outside scope ('<>' block survived parse strip): tag: {tag}\nscope: {scope[-1]}", scope, user_vars, frame_stack)
                        elif scope[-2]['scope_type'] == "#":
                            popped_scope = scope.pop()
                            # if close was a dot, invoke function before output
                            if char == '.':
                                scope.append({'scope_type':'.', 'token':'', 'close_char':'>', 'args':[tag]})
                                if 'varstore' in popped_scope:
                                    scope[-1]['varstore'] = popped_scope['varstore']
                            if 'tags' not in scope[-1]:
                                scope[-1]['tags'] = [tag]
                            else:
                                scope[-1]['tags'].append(tag)
                        # if close was a comma, chain
                        if char == ',':
                            scope.append({'scope_type':'<', 'token':''})
                    else:
                        scope[-1]['token'] += char

                # OPERATION EXECUTION
                elif scope[-1]['scope_type'] == '[':
                    if char == '#':
                        scope.append({'scope_type':'#', 'token':''})
                    elif char == '$':
                        scope.append({'scope_type':'$', 'token':''})
                    elif char == '<':
                        self.raise_parse_error(f"Illegal tag invocation in operation execution ('<' in '[]' block): {scope[-1]['token']}", scope, user_vars, frame_stack)
                    elif char == '[':
                        self.raise_parse_error(f"Illegal nested operation (open '[' in '[]' block): {scope[-1]['token']}", scope, user_vars, frame_stack)
                    elif char == ':':
                        # previous is a var store
                        scope[-1]['varstore'] = scope[-1]['token']
                        scope[-1]['token'] = ''
                    elif char in '],.':
                        popped_scope = scope.pop()
                        exec_ret = popped_scope['token']
                        # if close was a dot, invoke function before output
                        if char == '.':
                            popped_scope['token'] = ''
                            scope.append({'scope_type':'.', 'token':'', 'close_char':']', 'args':[exec_ret]})
                            if 'varstore' in popped_scope:
                                scope[-1]['varstore'] = popped_scope['varstore']
                        else:
                            if 'varstore' in popped_scope:
                                user_vars[popped_scope['varstore']] = exec_ret
                            # if close was a comma, chain
                            if char == ',':
                                scope.append({'scope_type':'[', 'token':''})
                    else:
                        scope[-1]['token'] += char

                # FUNCTION INVOCATION
                elif scope[-1]['scope_type'] == '.':
                    if char == '(':
                        scope.append({'scope_type':'.(', 'token':''})
                    elif char == scope[-1]['close_char'] or char == ',' or char == '.':
                        popped_scope = scope.pop()
                        func_name = popped_scope['token']
                        func_to_exec = self.func_lib[func_name]
                        func_ret = func_to_exec(scope, frame_stack, user_vars, popped_scope['args'])
                        # if close was a dot, chain to another function
                        if char == '.':
                            scope.append({'scope_type':'.', 'token':'', 'close_char':popped_scope['close_char'], 'args':[func_ret]})
                            if 'varstore' in popped_scope:
                                scope[-1]['varstore'] = popped_scope['varstore']
                        else:
                            if popped_scope['close_char'] == '>':
                                # tags are not output
                                if 'tags' not in scope[-1]:
                                    scope[-1]['tags'] = [func_ret]
                                else:
                                    scope[-1]['tags'].append(func_ret)
                            elif popped_scope['close_char'] != ']':
                                scope[-1]['token'] += func_ret
                            if 'varstore' in popped_scope:
                                user_vars[popped_scope['varstore']] = func_ret
                            # if close was a comma, chain the invocation scope
                            if char == ',':
                                scope.append({'scope_type':popped_scope['close_char'], 'token':''})
                                if popped_scope['close_char'] == '>':
                                    scope[-1]['scope_type'] = '<'
                                if popped_scope['close_char'] == ']':
                                    scope[-1]['scope_type'] = '['
                    elif char in "#$<>[]:":
                        self.raise_parse_error(f"Illegal character '{char}' in function name '{scope[-1]['token']}'", scope, user_vars, frame_stack)
                    else:
                        scope[-1]['token'] += char

                # FUNCTION ARGUMENTS
                elif scope[-1]['scope_type'] == '.(':
                    if char in "#$<>[]:":
                        self.raise_parse_error(f"Illegal character '{char}' in function arguments '{scope[-1]['token']}'", scope, user_vars, frame_stack)
                    if char == ')':
                        # get args
                        popped_scope = scope.pop()
                        arg_str = popped_scope['token']
                        args = arg_str.split(',')

                        # get func
                        popped_scope = scope.pop()
                        func_name = popped_scope['token']
                        func_to_exec = self.func_lib[func_name]

                        # put parent_output back into args list
                        args = popped_scope['args'] + args

                        # execute
                        func_ret = func_to_exec(scope, frame_stack, user_vars, args)
                        # treat the character after the paren as our close
                        i += 1
                        char = exp[i]
                        if char == '.':
                            # pass output to next function if dot
                            scope.append({'scope_type':'.', 'token':'', 'close_char':popped_scope['close_char'], 'args':[func_ret]})
                            if 'varstore' in popped_scope:
                                scope[-1]['varstore'] = popped_scope['varstore']
                        elif char == popped_scope['close_char'] or char == ',' or char == '.':
                            if popped_scope['close_char'] == '>':
                                # tags are not output
                                if 'tags' not in scope[-1]:
                                    scope[-1]['tags'] = [func_ret]
                                else:
                                    scope[-1]['tags'].append(func_ret)
                            elif popped_scope['close_char'] != ']':
                                scope[-1]['token'] += func_ret
                            if 'varstore' in popped_scope:
                                user_vars[popped_scope['varstore']] = func_ret
                            # if close was a comma, chain the invocation scope
                            if char == ',':
                                scope.append({'scope_type':popped_scope['close_char'], 'token':''})
                                if popped_scope['close_char'] == '>':
                                    scope[-1]['scope_type'] = '<'
                                if popped_scope['close_char'] == ']':
                                    scope[-1]['scope_type'] = '['
                        else:
                            self.raise_parse_error(f"Function call not at end of invocation. Expression: {exp} function call: {popped_scope['close_char']}{args[0]}.{func_name}({str(args)[1:-1]}){char}", scope, user_vars, frame_stack)
                    else:
                        scope[-1]['token'] += char

                i += 1
        
        # output to higher level
        # print(f"FRAME EXIT\nUSER_VARS {user_vars}\nPARENT_STACK {parent_stack}\nOUTPUT {output}\n")
        if len(scope) != 1:
            self.raise_parse_error(f"Missing close", scope, user_vars, frame_stack)
        if scope[0]['scope_type'] != 'output':
            self.raise_parse_error(f"Impossible: Outermost scope is not output '{scope[-1]['scope_type']}'\ntoken: {scope[-1]['token']}", scope, user_vars, frame_stack)
        return scope[0]['token']

    def __make_exp_frame(self, exp, scope, i):
        frame = {}
        frame['exp'] = exp
        frame['scope'] = scope
        frame['i'] = i
        return frame

    def raise_parse_error(self, message, scope, user_vars, parent_stack):
        if len(parent_stack) > 0 and 'scope' in parent_stack[-1] and len(parent_stack[-1]['scope']) > 0 and 'token' in parent_stack[-1]['scope']:
            output = parent_stack[-1]['scope'][0]['token']
        else:
            output = "<INTERNAL ERR: Output DNE>"
        raise AttributeError(f"{message}\ncurrent output: {output}\ncurrent scope: {scope}\nuser_vars {user_vars}\nstack:{parent_stack}")

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