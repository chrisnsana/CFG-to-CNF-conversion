import json
import os

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
        print(self.productions)
        
        if generate_steps is True:
            # Get the file name without the path or extension (i.e. XXX.json)
            in_name  = os.path.splitext(os.path.basename(json_file))[0]
            # A simple text file will be created show casing all the steps.
            out_name = './output/' + in_name + '_steps.txt'
            self.output_file = open(out_name, 'w')


        # Perform the necessary steps to achieve Chomsky normal form.
        self.__eliminate_useless_symbols()
        

        


    def __write_step(self, step_description):
        # There is no output file and therefore nothing to do.
        if self.output_file is None:
            return


    def __eliminate_epsilon_transitions(self):
        """
        Eliminate all the epsilon rules, which are rules of the form A -> Ɛ
        (with A not being the start symbol of the grammar).
        """


    def __eliminate_unit_productions(self):
        """
        Eliminate all the unit productions. These are productions of the form
        A -> B with A and B being variables of the grammar.
        """

    def __is_non_generating(self, symbol):
        # Recursively determine if a symbol is non-generating.
        # Base case, there are no rules available for this symbol (key)

        if symbol not in self.productions:
            # A terminal is never non-generating
            if symbol in self.terminals:
                return False
            # A variable with no rules is always non-generating.
            elif symbol in self.variables:
                return True

        # Else there is a rule for the symbol, but it may contain other
        # symbols that are non-generating making itself non-generating.

        for rule in self.productions[symbol]:
            generating_rule = True
            for s in rule:
                if s == symbol : continue
                # If a rule contains even one non-generating symbol,
                # the whole rule becomes non-generating.
                if self.__is_non_generating(s) is True:
                    generating_rule = False
                    break

            # We found one rule that does generate something for this symbol
            # and that makes it generating.
            if generating_rule is True:
                return False

        #No generating rules found for this symbol, so it's non-generating.
        return True

    def __is_reachable(self, symbol):
        # Recursively determine if a symbol is reachable
        # Base case, the symbol is the start symbol or there
        # is a rule of the form S => ...symbol...
        if symbol == self.start:
            return True
        
        if (any(symbol in rule for rule in self.productions[self.start])):
            return True

        # Else there is a rule of the form A => symbol... and we have to
        # determine recursively if A is reachable to know if symbol is too.
        for key, value in self.productions.items():
            if (any(symbol in rule for rule in self.productions[key])):
                if key == symbol : continue
                
                if self.__is_reachable(key):
                    return True
        else:
            # No rule shows 'symbol' to be reachable.
            return False

    def __eliminate_non_generating(self):
        """
        Eliminate all variables that never lead to any terminals.
        """
        for var in self.variables.copy():
            if not self.__is_non_generating(var):
                #Ignore this variable, there is nothing to do for it.
                continue

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
        symbols = set().union(self.terminals, self.variables)
        for s in symbols:
            if self.__is_reachable(s):
                continue
            
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



    def __eliminate_useless_symbols(self):
        """
        Eliminate all the useless symbols. There are two categories of useless
        symbols: the variables that never lead to any terminals
        (non-generating) and the symbols that can't be reached from the start
        symbol with the present production rules (non-reachable).
        """
        self.__eliminate_non_generating()
        print(self.productions)
        self.__eliminate_non_reachable()

        
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
        


