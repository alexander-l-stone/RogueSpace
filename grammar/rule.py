from random import randint

class Rule:
    def __init__(self, name:str, expansions:list):
        self.name = name
        self.expansions = {} # str expansion -> tuple(int weight, array[str] tags)
        for exp in expansions:
            # if the string starts with a number and a %, strip that off as a weight
            numstr = ''
            inserted = False
            for char in exp:
                if char == '\\':
                    continue
                if not char.isdigit() and char != '%':
                    self.expansions[exp] = (1, {}, exp)
                    inserted = True
                    break
                if char != '%':
                    numstr += char
                elif numstr == '':
                    raise AttributeError(f"Null weight. Rule: {name} Expansion: {exp}")
                else:
                    self.expansions[exp[len(numstr)+1:]] = (int(numstr), {}, exp)
                    inserted = True
                    break
            if not inserted:
                self.expansions[exp] = (1, {}, exp)
        # strip tags and escapes
        changed_dict = {}
        for exp,data in self.expansions.items():
            exp_raw = exp
            exp_tagless = exp
            tag_ind = None
            tag_pct = None
            i = len(exp) - 1
            # from right to left:
            # find a '>' to start a tag
            # '%' marks a weight prefix
            # end the tag on a ',' (chain rule) or '<'
            # ignore special '&' and '^' logic, that will be parsed in select_child()
            # but ensure that '^' appears to the right of a tag delimiter [<,&]
            while i >= 0:
                char = exp[i]
                if i > 0 and exp[i-1] == '\\':
                    i -= 1 # skip the character after the \
                elif char == '>':
                    tag_ind = i
                elif tag_ind is not None:
                    if char in "#$>[].":
                        raise AttributeError(f"Illegal use of 'special character '{char}' inside tag. Rule: {name} Expansion: {exp_raw}")
                    if char == '%':
                        if tag_pct is not None:
                            raise AttributeError(f"Illegal second '%' inside tag. Rule: {name} Expansion: {exp_raw}")
                        tag_pct = i
                    if char == '^':
                        # ensure negation is at tag start
                        if i == 0:
                            break # hit unclosed tag error below
                        elif exp[i-1] not in '<,&%':
                            raise AttributeError(f"Tag negation not at start of tag. Rule: {name} Expansion: {exp_raw}")
                    if char == '<' or char == ',':
                        weight = None
                        if tag_pct is None:
                            tag_pct = i
                        else:
                            # TODO pretty print int format error
                            weight = int(exp[i+1:tag_pct])
                        # strip out the weight
                        tag = exp[tag_pct+1:tag_ind]
                        data[1][tag] = weight
                        # remove the weight from the tag
                        if tag_pct is not None:
                            exp = f"{exp[0:i+1]}{exp[tag_pct+1:]}"
                        # strip the whole tag out of the tagless variant to be returned as an expansion option
                        exp_tagless = f"{exp_tagless[0:i]}{exp_tagless[tag_ind+1:]}"
                        # chain comma clears weight pointer and sets end pointer to comma
                        if char == ',':
                            tag_ind = i
                        else:
                            tag_ind = None
                        tag_pct = None
                else:
                    # TODO maybe actually parse the whole exp and warn on mid-string tags?
                    # TODO parse enough to detect no unclosed tag (means finding at least an unescaped special char)
                    break
                i -= 1
            
            if tag_ind is not None:
                raise AttributeError(f"Unopened tag in rule '{name}'. Expansion: {exp_raw}")
            data = (data[0], data[1], exp_tagless)

            # check for duplicate keys and merge the entries
            if exp in changed_dict:
                # TODO add suppress warning option?
                # TODO output print to a logger?
                print(f"WARNING: Identical expression appears multiple times in rule '{name}'. Expansion: {exp}")
                tag_dict = changed_dict[exp][1]
                # we should always have the same tags
                if tag_dict.keys() == data[1].keys():
                    # add the weights of identical tags, otherwise merge tags
                    for tag,tag_weight in data[1].items():
                        if tag in tag_dict:
                            tag_dict[tag] += tag_weight
                else:
                    raise AttributeError(f"Expansions with identical tags had nonidentical tags! tags1: {tag_dict} tags2: {data[1]} Rule: {name} Expansion: {exp}")
                data = (changed_dict[exp][0] + data[0], tag_dict, exp_tagless)
            
            # add self to the new dict so we don't need to modify the old one during iteration
            changed_dict[exp] = data
        self.expansions = changed_dict

    def select_child(self, invoked_tags:dict=[])->str:
        '''
        Randomly select an expansion by weight
        If a tag is provided, only consider expansions which have that tag
        '''
        total_weight = 0
        for exp,data in self.expansions.items():
            # do not add weight for tagged exp without invoked tag block
            if not self.__include_exp(data[1], invoked_tags):
                continue

            weight = self.__get_weight(data[0], data[1], invoked_tags)
            # exp contributes its weight to generation
            total_weight += weight

        if total_weight == 0:
            raise AttributeError(f"No valid expansions for tags {invoked_tags} in rule {self}")

        rand = randint(1, total_weight)
        for exp,data in self.expansions.items():
            # do not count weight for tagged exp without invoked tag block
            if not self.__include_exp(data[1], invoked_tags):
                continue

            weight = self.__get_weight(data[0], data[1], invoked_tags)
            rand -= weight
            # did we land in weight band for this exp
            if rand <= 0:
                return data[2]
        # unreachable
        return None

    def __get_weight(self, base_weight, tag_data, invoked_tags):
        '''
        use base weight if no tags
        otherwise return weight of the last invoked tag
        '''
        if invoked_tags:
            for i in range(len(invoked_tags) - 1, -1, -1):
                if invoked_tags[i] in tag_data and tag_data[invoked_tags[i]] is not None:
                    return tag_data[invoked_tags[i]]
        return base_weight

    def __include_exp(self, exp_tag_blocks, invoked_tags):
        if exp_tag_blocks:
            inv_matched = dict((inv_tag,False) for inv_tag in invoked_tags)

            skip_expansion = True
            for exp_tag_block in exp_tag_blocks:
                tag_satisfied = True
                for exp_tag in exp_tag_block.split('&'):
                    # each positive exp tag must find a match
                    positive_matched = False
                    for inv_tag in invoked_tags:
                        # Strip a leading '^' and mark that argument as negative
                        exp_neg = False
                        inv_neg = False
                        if exp_tag[0] == '^':
                            exp_neg = True
                            exp_tag = exp_tag[1:]
                        if inv_tag[0] == '^':
                            inv_neg = True
                            inv_tag = inv_tag[1:]
                        print(f"exp ({'neg' if exp_neg else 'pos'}) {exp_tag}\ninv ({'neg' if inv_neg else 'pos'}) {inv_tag}")
                        # Negative declarations and invocations are not tags and do not interact; valid combination (see below)
                        if exp_neg and inv_neg:
                            print(f"both neg, continue")
                            continue
                        # A negated tag declation is invalidated if a positive tag invocation is present
                        # A negated tag invocation is invalidated if a positive tag declation is present
                        if exp_neg or inv_neg and exp_tag == inv_tag:
                            tag_satisfied = False
                            print(f"one neg and match, fail")
                            break
                        # A positive tag declatation is satisfied if an invocation tag is present
                        if not exp_neg and exp_tag == inv_tag:
                            print(f"pos exp and match, succeed")
                            positive_matched = True
                            print(f"inv_tag '{inv_tag}' inv_matched {inv_matched}")
                            inv_matched[inv_tag] = True
                            print(f'post inv_matched {inv_matched}')
                            break
                        # continue implicitly to next invoked tag
                    if not positive_matched:
                        tag_satisfied = False
                        print(f'positive was not matched, fail')
                    print(f'tag_satisfied? {tag_satisfied}\n\n')
                    if not tag_satisfied:
                        break
                if tag_satisfied:
                    skip_expansion = False
            
            print(f'post exp parse inv_matched {inv_matched}')
            for inv_tag,matched in inv_matched.items():
                if not matched:
                    print(f'not matched: {inv_tag}')
                    skip_expansion = True
                    break
            print(f'skip_expansion? {skip_expansion}')
            if skip_expansion:
                print("return false")
                return False
            print("return true")
        return True
    
    def __repr__(self):
        return '"' + self.name + '" : ' + str(self.expansions)

    def __str__(self):
        return '"' + self.name + '" : ' + str(self.expansions)