import math

'''
    Grammar = file
    
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
    \ escape char
    #rule.func(arg)# apply a function to a rule (with arguments)
    #$varOfRule$# not technically a syntax - replaces var with value and evaluates as a rule name
    #prefix$postfix$# complexity!
    2% weight the following at 2 (default weight is 1)

    reserved chars
    \[]:#$%<>
'''

def read_grammar(self, fileName):
    '''
    throws FileNotFoundException
    '''
    with open(fileName, 'rb') as grammar_file:
        #TODO parse text file, output a Grammar
        pass

class Grammar:
    # TODO how are grammars created/loaded/invoked?
    def __init__(self, root):
        self.userVars = {}
        self.root = root
        self.rules = {} # name to obj
        ## TODO parse weights?

    def expand_rule(self, rule):
        # TODO implement
        # weight should be preparsed
        # pick an expansion at random
        # parse out the rule invocations, variable assignments, function invocations, etc
        # execute and recurse as necessary
        pass

    def parse_dollar(self, text, index):
        '''
        parse the inside of a variable unpacking
        index is the index of the open dollar
        '''
        pass

class Rule:
    # TODO how are rules loaded
    def __init__(self, name, *expansions):
        self.name = name
        self.expansions = expansions
        # TODO parse weight from expansions?

    def select_child(self):
        # TODO weight each entry and select at random
        pass
