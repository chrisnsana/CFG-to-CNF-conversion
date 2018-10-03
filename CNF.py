import json
import os
import itertools

from CFG import CFG



class CNF(CFG):
    """
    Class that represents a context-free grammar in Chomsky normal form (CNF).
    """

    def __init__(self, json_file, generate_steps):
        """
        Constructs a CNF object by reading a json file with the expected format.

        Parameters:
            json_file: The name of which json_file we're using for construction.
            generate_steps: Boolean indicating if the constructor should
                            create an output file with all the steps needed
                            to convert to Chomsky normal form.
                            True generates the file, False does not.
        """
        # Construct the context-free grammar as described in the file before
        # the conversion to Chomsky normal form happens.
        super().__init__(json_file)
        self.generate_steps = generate_steps
        self.output_file    = None
        self.var_count      = 1 # Used for self created variables.
        
        if generate_steps is True:
            # Get the file name without the path or extension (i.e. XXX.json)
            in_name  = os.path.splitext(os.path.basename(json_file))[0]
            # A simple text file will be created show casing all the steps.
            out_name = './output/' + in_name + '_steps.txt'
            self.output_file = open(out_name, 'w')


        # Perform the necessary steps to achieve Chomsky normal form.
        self.__eliminate_epsilon_transitions()
        self.__eliminate_unit_productions()
        self.__eliminate_useless_symbols()
        self.__arrange_variable_bodies()
        self.__break_long_bodies()

        if self.generate_steps is True:
            self.output_file.close()
        
    def __write_step(self, step_description):
        # There is no output file and therefore nothing to do.
        if self.output_file is None:
            return

        self.output_file.write(step_description)
        self.output_file.write('\n')
        # print out variables
        vars_str = 'variables: ' + str(self.variables)
        term_str = 'terminals: ' + str(self.terminals)
        prod_str = 'productions:\n'
        self.output_file.write(vars_str)
        self.output_file.write('\n')
        self.output_file.write(term_str)
        self.output_file.write('\n')
        self.output_file.write(prod_str)
   
        for key, value in self.productions.items():
            for rule in value:
                line = key + ' => ' + str(rule)
                self.output_file.write(line)
                self.output_file.write('\n')

        self.output_file.write('\n')
    

    def __eliminate_epsilon_transitions(self):
        """
        Eliminate all the epsilon rules, which are rules of the form A => Ɛ
        (with A not being the start symbol of the grammar).
        """
        nullables = self.__find_nullables()

        for key in self.productions:
            for rule in self.productions[key].copy():
                if(any(symbol in nullables for symbol in rule)):
                    unaffected = list(s for s in rule if s not in nullables)
                    powerset   = self.__get_powerset(rule)
                    new_rules  = set()
                    for n_rule in (x for x in powerset if len(x) > 0):
                        if (all(u in n_rule for u in unaffected)):
                            new_rules.add(n_rule)

                    # Add these newly generated rules.
                    self.productions[key].update(new_rules)

                elif len(rule) == 0:
                    # This case deletes the rule of the form A => Ɛ
                    self.productions[key].remove(rule)

        self.__write_step('ELIMINATING EPSILON TRANSITIONS')
                
    def __eliminate_unit_productions(self):
        """
        Eliminate all the unit productions. These are productions of the form
        A => B with A and B being variables of the grammar.
        """
        unit_pairs      = [(var, var) for var in self.variables]
        new_productions = dict()

        # Create more unit pair from the base ones.
        for pair in unit_pairs:
            first  = pair[0]
            second = pair[1]
            # We are not certaj  that every variable is generating.
            rules  = self.productions.get(second, [])
            for s in rules:
                if len(s) == 1 and s[0] in self.variables:
                    unit_pairs.append((first, s[0]))

        print(unit_pairs)
        # Now loop over the complete list of unit pairs to create the
        # new productions by eliminating unit productions.
        for pair in unit_pairs:
            first  = pair[0]
            second = pair[1]
            if second not in new_productions:
                new_productions[second] = set()

            # We are not certain that every variable is generating.
            for rule in self.productions.get(second, []):
                if len(rule) == 1 and rule[0] in self.variables:
                    # We don't want re-add the unit productions.
                    continue
                
                new_productions[first].add(rule)

        # Replace the old productions with new ones without unit productions.
        self.productions = new_productions
        self.__write_step('ELIMINATING UNIT PRODUCTIONS')

    def __eliminate_useless_symbols(self):
        """
        Eliminate all the useless symbols. There are two categories of useless
        symbols: the variables that never lead to any terminals
        (non-generating) and the symbols that can't be reached from the start
        symbol with the present production rules (non-reachable).
        """
        self.__eliminate_non_generating()
        self.__eliminate_non_reachable()
        self.__write_step('ELIMINATING USELESS SYMBOLS')

    def __eliminate_non_generating(self):
        """
        Eliminate all variables that never lead to any terminals.
        """
        non_generating = self.__find_non_generating()
        for var in non_generating:
            # Delete all the rules for this variable
            self.productions.pop(var, None)

            # Delete all the rules containing this variable
            for key in self.productions.copy():
                for rule in self.productions[key].copy():
                    if var in rule: self.productions[key].remove(rule)

            # Delete the variable from list of variables.
            self.variables.remove(var)

    def __eliminate_non_reachable(self):
        """
        Eliminate all symbols that can't be reached from the start symbol.
        """
        non_reachables = self.__find_non_reachable()
        for s in non_reachables:
            # Delete all the rules for this symbol (if present)
            self.productions.pop(s, None)

            # Delete all the rules containing this variable
            for key in self.productions.copy():
                for rule in self.productions[key].copy():
                    if s in rule: self.productions[key].remove(rule)

            # Delete the symbol from the correct set
            if s in self.variables:
                self.variables.remove(s)
                
            elif s in self.terminals:
                self.terminals.remove(s)

    def __arrange_variable_bodies(self):
        """
        Substitute terminals in bodies of length > 1 with newly made variables.
        A => Bb will become A => BC and a new rule C => b will be added.
        """
        for key, value in self.productions.copy().items():
            for rule in value:
                if len(rule) > 1 and (any(r in self.terminals for r in rule)):
                    seen_terminals = dict()
                    rule_2         = list(rule)
                    for symbol in rule_2:
                        if symbol in self.terminals :
                            new_var = "T" + str(self.var_count)
                            # In the special case the variable already exists
                            while new_var in self.variables:
                                self.var_count += 1
                                new_var         = "T" + str(self.var_count)

                            self.var_count += 1
                            self.variables.add(new_var)
                            seen_terminals[symbol] = new_var

                    for key2, value2 in seen_terminals.items():
                        self.productions[value2] = (key2,)

                    modified_rule = [seen_terminals.get(x, x) for x in rule_2]
                    modified_rule = tuple(modified_rule)
                    self.productions[key].remove(rule)
                    self.productions[key].add(modified_rule)

        self.__write_step('MAKING BODIES OF LENGTH >= 2 CONSIST OF VARIABLES')

    def __break_long_bodies(self):
        """
        Break up long bodies of length > 2 in several bodies of 2 variables.
        A => BCD will be split up in  A => BE and E => CD for example.
        """
        for key, value in self.productions.copy().items():
            for rule in value:
                if len(rule) > 2:
                    var_list = list(rule)
                    left_var = key
                    while len(var_list) > 2:
                        new_var = "T" + str(self.var_count)
                        # In the special case the variable already exists
                        while new_var in self.variables:
                            self.var_count += 1
                            new_var         = "T" + str(self.var_count)

                        self.var_count += 1
                        self.variables.add(new_var)
                        
                        body = (left_var, var_list[0])
                        if left_var not in self.productions:
                            self.productions[left_var] = set()

                        self.productions[left_var].add(body)
                        # Continue splitting up using the second var
                        left_var = new_var
                        var_list = var_list[1:]

                    self.productions[key].remove(rule)
                    
        self.__write_step('BREAKING UP BODIES OF LENGTH > 2.')

    def __find_nullables(self):
        nullables = []
        # Base: find all variables with epsilon transitions
        for key, value in self.productions.items():
            # If there is an epsilon transition
            if(any(len(rule) == 0 for rule in value)):
                nullables.append(key)

        if len(nullables) == 0:
            return []
        
        for key, value in self.productions.items():
            for rule in value:
                if all(s in nullables for s in rule):
                    nullables.append(key)

        return nullables
    
    def __find_non_generating(self):
        non_generating = []
        for var in self.variables:
            # A variable with no rule that generates anything.
            if var not in self.productions:
                non_generating.append(var)

        for key, value in self.productions.items():
            generating = False
            for rule in value:
                # If a rule contains all generating symbols
                if (all(r not in non_generating for r in rule)):
                    # Even just one generating rule makes it generating.
                    generating = True

            if generating is False:
                non_generating.append(key)

        return non_generating

    def __find_non_reachable(self):
        reachables = [self.start]
        # Iteratively calculate all reachables
        for r in reachables:
            rules = {}
            if r in self.variables:
                rules = self.productions[r]
            for rule in rules:
                for symbol in rule:
                    if symbol not in reachables: reachables.append(symbol)

        all_symbols = set().union(self.variables, self.terminals)
        # Return difference between the two.
        return all_symbols - set(reachables)
                
    def __get_powerset(self, iterable):
        # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s     = list(iterable)
        chain =  itertools.chain.from_iterable(itertools.combinations(s, r)
                                               for r in range(len(s)+1))
        return list(chain)
                            
    def write_to_json(self, filename):
        """
        Write the grammar which is in Chomsky normal form to a json file in the
        format used throughout this project.
        """
        out_name = './output/' + filename
        with open(out_name, 'w') as out_file:
                data = dict()
                data["Variables"]   = list(self.variables)
                data["Terminals"]   = list(self.terminals)
                list_productions    = dict()
                # A set of tuples is not JSON serializable, so convert
                # the productions to list of lists
                for key, value in self.productions.items():
                    list_value            = [list(i) for i in value]
                    list_productions[key] = list_value
                
                data["Productions"] = list_productions
                data["Start"]       = self.start
                json.dump(data, out_file, ensure_ascii=False)
