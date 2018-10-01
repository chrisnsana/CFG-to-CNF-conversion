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

    def __eliminate_non_generating(self):
        """
        Eliminate all variables that never lead to any terminals.
        """
        for var in self.variables:
            if not self.__is_non_generating(var):
                #Ignore this variable, there is nothing to do for it.
                continue

            # Delete all the rules for this variable
            self.productions.pop(var, None)

            # Delete all the rules containing this variable
            for key in self.productions:
                for rule in self.productions[key]:
                    if var in rule: self.productions[key].remove(rule)

            # Delete the variable from list of variables.
            self.variables.remove(var)

    def __eliminate_non_reachable(self):
        """
        Eliminate all symbols that can't be reached from the start symbol.
        """
        pass



    def __eliminate_useless_symbols(self):
        """
        Eliminate all the useless symbols. There are two categories of useless
        symbols: the variables that never lead to any terminals
        (non-generating) and the symbols that can't be reached from the start
        symbol with the present production rules (non-reachable).
        """
        self.__eliminate_non_generating()
        self.__eliminate_non_reachable()

        
    def write_to_json(self, filename):
        """
        Write the grammar which is in Chomsky normal form to a json file in the
        format used throughout this project.
        """
        out_name = './output/' + filename
        with open(out_name, 'w') as out_file:
                data = dict()
                data["Variables"]   = self.variables
                data["Terminals"]   = self.terminals
                data["Productions"] = self.productions
                data["Start"]       = self.start
                json.dump(data, out_file, ensure_ascii=False)
        


