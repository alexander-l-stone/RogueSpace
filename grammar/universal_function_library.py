

def capitalize(scope, parent_stack, user_vars, args):
    return args[0].capitalize()
    
def remove(scope, parent_stack, user_vars, args):
    parent_output = args[0]
    substring = args[1]
    index = parent_output.find(substring)
    if index > -1:
        return parent_output[0:index] + parent_output[index+len(substring):]
    return parent_output