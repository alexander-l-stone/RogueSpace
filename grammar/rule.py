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
                    self.expansions[exp] = (1, {})
                    inserted = True
                    break
                if char != '%':
                    numstr += char
                elif numstr == '':
                    raise AttributeError(f"Null weight. Rule: {name} Expansion: {exp}")
                else:
                    self.expansions[exp[len(numstr)+1:]] = (int(numstr), {})
                    inserted = True
                    break
            if not inserted:
                self.expansions[exp] = (1, {})
        # strip tags and escapes
        changed_dict = {}
        for exp,data in self.expansions.items():
            tag_ind = None
            tag_pct = None
            i = len(exp) - 1
            while i >= 0:
                char = exp[i]
                if i > 0 and exp[i-1] == '\\':
                    i -= 1 # skip the character after the \
                elif char == '>':
                    tag_ind = i
                elif tag_ind is not None:
                    if char in "#$>[].":
                        raise AttributeError(f"Illegal use of 'special character '{char}' inside tag. Rule: {name} Expansion: {exp}")
                    if char == '%':
                        if tag_pct is not None:
                            raise AttributeError(f"Illegal second '%' inside tag. Rule: {name} Expansion: {exp}")
                        tag_pct = i
                    if char == '<':
                        weight = None
                        if tag_pct is None:
                            tag_pct = i
                        else:
                            weight = int(exp[i+1:tag_pct])
                        data[1][exp[tag_pct+1:tag_ind]] = weight
                        exp = exp[0:i] + exp[tag_ind+1:]
                        tag_ind = None
                        tag_pct = None
                else:
                    # TODO maybe actually parse the whole exp and warn on mid-string tags?
                    break
                i -= 1
            # add self to the new dict so we don't need to modify the old one during iteration
            changed_dict[exp] = data
        self.expansions = changed_dict

    def select_child(self, tags=None)->str:
        '''
        Randomly select an expansion by weight
        If a tag is provided, only consider expansions which have that tag
        '''
        total_weight = 0
        for exp,data in self.expansions.items():
            # do not add weight for exp without required tags
            if tags is not None:
                should_continue = False
                for tag in tags:
                    if tag not in data[1]:
                        should_continue = True
                        continue
                if should_continue:
                    continue

            # use weight of last tag, if present
            weight = data[0]
            if tags is not None and len(tags) > 0:
                for i in range(len(tags) - 1, -1, -1):
                    tag_weight = data[1][tags[i]]
                    if tag_weight is not None:
                        weight = tag_weight
                        break
            # exp contributes its weight to generation
            total_weight += weight

        if total_weight == 0:
            raise AttributeError(f"No valid expansions for tags {tags} in rule {self}")

        rand = randint(1, total_weight)
        for exp,data in self.expansions.items():
            # do not count weight for exp without required tags
            if tags is not None:
                should_continue = False
                for tag in tags:
                    if tag not in data[1]:
                        should_continue = True
                        continue
                if should_continue:
                    continue

            # use weight of last tag, if present
            weight = data[0]
            if tags is not None and len(tags) > 0:
                for i in range(len(tags) - 1, -1, -1):
                    tag_weight = data[1][tags[i]]
                    if tag_weight is not None:
                        weight = tag_weight
                        break
            rand -= weight
            # did we land in weight band for this exp
            if rand <= 0:
                return exp
        # unreachable
        return None
    
    def __repr__(self):
        return '"' + self.name + '" : ' + str(self.expansions)

    def __str__(self):
        return '"' + self.name + '" : ' + str(self.expansions)